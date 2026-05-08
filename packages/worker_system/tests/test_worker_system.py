"""Tests for Phase 15 worker system: job schemas, lifecycle, safety gates, queue, and worker."""
from __future__ import annotations

import os
import unittest

from packages.worker_system.jobs import (
    DEFAULT_SCAN_MAX_TESTS,
    JobPayload,
    JobResult,
    JobStatus,
    JobType,
    contains_secret_looking_fields,
    create_job_payload,
    is_valid_transition,
)
from packages.worker_system.queue import LocalMemoryQueue
from packages.worker_system.safety import SafetyGateResult, check_safety_gates
from packages.worker_system.worker import WorkerConfig, WorkerEngine


class JobPayloadTests(unittest.TestCase):
    def test_create_job_payload_generates_uuid(self) -> None:
        payload = create_job_payload(JobType.SCAN_RUN)
        self.assertTrue(len(payload.job_id) > 0)
        self.assertEqual(payload.job_type, "scan.run")

    def test_payload_round_trip(self) -> None:
        payload = create_job_payload(
            JobType.SCAN_RUN,
            project_id="proj-1",
            target_id="tgt-1",
            scan_type="safe_smoke",
            verification_status="verified",
        )
        data = payload.to_dict()
        restored = JobPayload.from_dict(data)
        self.assertEqual(restored.job_id, payload.job_id)
        self.assertEqual(restored.project_id, "proj-1")
        self.assertEqual(restored.verification_status, "verified")

    def test_result_round_trip(self) -> None:
        result = JobResult(
            job_id="test-123",
            status=JobStatus.COMPLETED,
            duration_ms=42,
            summary={"tests": 3},
        )
        data = result.to_dict()
        restored = JobResult.from_dict(data)
        self.assertEqual(restored.job_id, "test-123")
        self.assertEqual(restored.status, "completed")
        self.assertEqual(restored.duration_ms, 42)

    def test_all_job_types_defined(self) -> None:
        self.assertIn("scan.run", JobType.ALL)
        self.assertIn("scan.evaluate", JobType.ALL)
        self.assertIn("scan.summarize", JobType.ALL)
        self.assertIn("report.prepare_placeholder", JobType.ALL)

    def test_all_job_statuses_defined(self) -> None:
        self.assertIn("queued", JobStatus.ALL)
        self.assertIn("running", JobStatus.ALL)
        self.assertIn("completed", JobStatus.ALL)
        self.assertIn("failed", JobStatus.ALL)
        self.assertIn("cancelled", JobStatus.ALL)
        self.assertIn("timed_out", JobStatus.ALL)
        self.assertIn("blocked_unverified", JobStatus.ALL)
        self.assertIn("blocked_unsafe", JobStatus.ALL)

    def test_terminal_states(self) -> None:
        for status in JobStatus.TERMINAL:
            self.assertIn(status, JobStatus.ALL)
        self.assertNotIn("queued", JobStatus.TERMINAL)
        self.assertNotIn("running", JobStatus.TERMINAL)


class LifecycleTransitionTests(unittest.TestCase):
    def test_queued_to_running(self) -> None:
        self.assertTrue(is_valid_transition("queued", "running"))

    def test_queued_to_cancelled(self) -> None:
        self.assertTrue(is_valid_transition("queued", "cancelled"))

    def test_queued_to_blocked_unverified(self) -> None:
        self.assertTrue(is_valid_transition("queued", "blocked_unverified"))

    def test_queued_to_blocked_unsafe(self) -> None:
        self.assertTrue(is_valid_transition("queued", "blocked_unsafe"))

    def test_running_to_completed(self) -> None:
        self.assertTrue(is_valid_transition("running", "completed"))

    def test_running_to_failed(self) -> None:
        self.assertTrue(is_valid_transition("running", "failed"))

    def test_running_to_timed_out(self) -> None:
        self.assertTrue(is_valid_transition("running", "timed_out"))

    def test_invalid_completed_to_running(self) -> None:
        self.assertFalse(is_valid_transition("completed", "running"))

    def test_invalid_failed_to_running(self) -> None:
        self.assertFalse(is_valid_transition("failed", "running"))

    def test_invalid_queued_to_completed(self) -> None:
        self.assertFalse(is_valid_transition("queued", "completed"))


class SecretFieldDetectionTests(unittest.TestCase):
    def test_detects_api_key(self) -> None:
        data = {"api_key": "sk-12345"}
        flagged = contains_secret_looking_fields(data)
        self.assertEqual(len(flagged), 1)
        self.assertIn("api_key", flagged[0])

    def test_detects_nested_bearer_token(self) -> None:
        data = {"auth": {"bearer_token": "abc"}}
        flagged = contains_secret_looking_fields(data)
        self.assertEqual(len(flagged), 1)
        self.assertIn("bearer_token", flagged[0])

    def test_detects_password(self) -> None:
        data = {"password": "secret123"}
        flagged = contains_secret_looking_fields(data)
        self.assertTrue(len(flagged) >= 1)

    def test_clean_payload_passes(self) -> None:
        data = {"name": "My Target", "type": "mock", "notes": "safe"}
        flagged = contains_secret_looking_fields(data)
        self.assertEqual(len(flagged), 0)

    def test_detects_multiple_secrets(self) -> None:
        data = {"api_key": "x", "private_key": "y", "cookie": "z"}
        flagged = contains_secret_looking_fields(data)
        self.assertEqual(len(flagged), 3)


class SafetyGateTests(unittest.TestCase):
    def _make_safe_payload(self, **overrides: object) -> JobPayload:
        defaults = {
            "job_type": JobType.SCAN_RUN,
            "verification_status": "verified",
            "scan_type": "safe_smoke",
            "target_snapshot": {"name": "Mock Target", "type": "mock"},
            "limits": {"max_tests": 3, "timeout_seconds": 10},
        }
        defaults.update(overrides)
        return create_job_payload(**defaults)

    def test_safe_payload_passes_all_gates(self) -> None:
        payload = self._make_safe_payload()
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertTrue(result.passed)

    def test_unverified_target_blocked(self) -> None:
        payload = self._make_safe_payload(verification_status="unverified")
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)
        self.assertIn("verification", result.blocked_reason.lower())

    def test_pending_verification_blocked(self) -> None:
        payload = self._make_safe_payload(verification_status="pending")
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)

    def test_unknown_job_type_blocked(self) -> None:
        payload = self._make_safe_payload()
        payload.job_type = "unknown.bad_type"
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)
        self.assertIn("not recognized", result.blocked_reason)

    def test_localhost_url_blocked(self) -> None:
        payload = self._make_safe_payload(
            scan_type="standard",
            target_snapshot={"name": "Bad", "endpoint_url": "http://localhost:8080/api"},
        )
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)
        self.assertIn("private", result.blocked_reason.lower())

    def test_internal_ip_blocked(self) -> None:
        payload = self._make_safe_payload(
            scan_type="standard",
            target_snapshot={"name": "Bad", "endpoint_url": "http://192.168.1.1/api"},
        )
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)

    def test_metadata_ip_blocked(self) -> None:
        payload = self._make_safe_payload(
            scan_type="standard",
            target_snapshot={"name": "Bad", "endpoint_url": "http://169.254.169.254/latest/meta-data/"},
        )
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)

    def test_secret_fields_blocked(self) -> None:
        payload = self._make_safe_payload(
            target_snapshot={"name": "Target", "api_key": "sk-12345"},
        )
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)
        self.assertIn("secret", result.blocked_reason.lower())

    def test_excessive_max_tests_blocked(self) -> None:
        payload = self._make_safe_payload(limits={"max_tests": 9999, "timeout_seconds": 10})
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)
        self.assertIn("max_tests", result.blocked_reason)

    def test_excessive_timeout_blocked(self) -> None:
        payload = self._make_safe_payload(limits={"max_tests": 3, "timeout_seconds": 99999})
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        self.assertFalse(result.passed)
        self.assertIn("timeout", result.blocked_reason.lower())

    def test_queue_disabled_blocks(self) -> None:
        saved = os.environ.get("WORKER_ENABLED")
        os.environ["WORKER_ENABLED"] = "false"
        try:
            payload = self._make_safe_payload()
            result = check_safety_gates(payload, skip_queue_enabled_check=False)
            self.assertFalse(result.passed)
            self.assertIn("WORKER_ENABLED", result.blocked_reason)
        finally:
            if saved is None:
                os.environ.pop("WORKER_ENABLED", None)
            else:
                os.environ["WORKER_ENABLED"] = saved

    def test_gate_result_serializes(self) -> None:
        payload = self._make_safe_payload()
        result = check_safety_gates(payload, skip_queue_enabled_check=True)
        data = result.to_dict()
        self.assertIn("passed", data)
        self.assertIn("gate_results", data)
        self.assertIsInstance(data["gate_results"], list)


class LocalMemoryQueueTests(unittest.TestCase):
    def test_enqueue_dequeue_cycle(self) -> None:
        queue = LocalMemoryQueue()
        payload = create_job_payload(JobType.SCAN_RUN)
        queue.enqueue(payload)
        self.assertEqual(queue.pending_count(), 1)
        dequeued = queue.dequeue()
        self.assertIsNotNone(dequeued)
        self.assertEqual(dequeued.job_id, payload.job_id)
        self.assertEqual(queue.pending_count(), 0)

    def test_dequeue_empty_returns_none(self) -> None:
        queue = LocalMemoryQueue()
        self.assertIsNone(queue.dequeue())

    def test_status_tracking(self) -> None:
        queue = LocalMemoryQueue()
        payload = create_job_payload(JobType.SCAN_RUN)
        queue.enqueue(payload)
        self.assertEqual(queue.get_status(payload.job_id), "queued")
        queue.dequeue()
        self.assertEqual(queue.get_status(payload.job_id), "running")

    def test_store_and_get_result(self) -> None:
        queue = LocalMemoryQueue()
        result = JobResult(job_id="test-1", status=JobStatus.COMPLETED)
        queue.store_result(result)
        retrieved = queue.get_result("test-1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.status, "completed")

    def test_list_jobs(self) -> None:
        queue = LocalMemoryQueue()
        p1 = create_job_payload(JobType.SCAN_RUN)
        p2 = create_job_payload(JobType.SCAN_EVALUATE)
        queue.enqueue(p1)
        queue.enqueue(p2)
        jobs = queue.list_jobs()
        self.assertEqual(len(jobs), 2)


class WorkerEngineTests(unittest.TestCase):
    def test_mock_scan_run_completes(self) -> None:
        payload = create_job_payload(
            JobType.SCAN_RUN,
            verification_status="verified",
            scan_type="safe_smoke",
            target_snapshot={"name": "Test Mock", "type": "mock"},
            limits={"max_tests": 2, "timeout_seconds": 10},
        )
        config = WorkerConfig(output_dir="worker-output", dry_run=True)
        engine = WorkerEngine(config=config)
        result = engine.execute(payload)
        self.assertEqual(result.status, JobStatus.COMPLETED)
        self.assertIn("scan_id", result.metadata)
        self.assertFalse(result.metadata.get("network_used", True))

    def test_unverified_payload_blocked_by_worker(self) -> None:
        payload = create_job_payload(
            JobType.SCAN_RUN,
            verification_status="unverified",
            target_snapshot={"name": "Test", "type": "mock"},
        )
        config = WorkerConfig(dry_run=True)
        engine = WorkerEngine(config=config)
        result = engine.execute(payload)
        self.assertEqual(result.status, JobStatus.BLOCKED_UNVERIFIED)

    def test_placeholder_job_types_complete(self) -> None:
        for job_type in [JobType.SCAN_EVALUATE, JobType.SCAN_SUMMARIZE, JobType.REPORT_PREPARE_PLACEHOLDER]:
            payload = create_job_payload(
                job_type,
                verification_status="verified",
                target_snapshot={"name": "Test", "type": "mock"},
                limits={"max_tests": 3, "timeout_seconds": 10},
            )
            config = WorkerConfig(dry_run=True)
            engine = WorkerEngine(config=config)
            result = engine.execute(payload)
            self.assertEqual(result.status, JobStatus.COMPLETED, f"Failed for {job_type}")

    def test_process_next_from_queue(self) -> None:
        queue = LocalMemoryQueue()
        payload = create_job_payload(
            JobType.SCAN_RUN,
            verification_status="verified",
            target_snapshot={"name": "Test", "type": "mock"},
            limits={"max_tests": 2, "timeout_seconds": 10},
        )
        queue.enqueue(payload)
        config = WorkerConfig(output_dir="worker-output", dry_run=True)
        engine = WorkerEngine(queue=queue, config=config)
        result = engine.process_next()
        self.assertIsNotNone(result)
        self.assertEqual(result.status, JobStatus.COMPLETED)

    def test_process_next_empty_queue(self) -> None:
        engine = WorkerEngine(config=WorkerConfig(dry_run=True))
        result = engine.process_next()
        self.assertIsNone(result)

    def test_result_shape(self) -> None:
        payload = create_job_payload(
            JobType.SCAN_RUN,
            verification_status="verified",
            target_snapshot={"name": "Test", "type": "mock"},
            limits={"max_tests": 2, "timeout_seconds": 10},
        )
        config = WorkerConfig(dry_run=True)
        engine = WorkerEngine(config=config)
        result = engine.execute(payload)
        data = result.to_dict()
        self.assertIn("job_id", data)
        self.assertIn("status", data)
        self.assertIn("started_at", data)
        self.assertIn("completed_at", data)
        self.assertIn("duration_ms", data)
        self.assertIn("summary", data)
        self.assertIn("safety_decision", data)
        self.assertIn("metadata", data)


if __name__ == "__main__":
    unittest.main()
