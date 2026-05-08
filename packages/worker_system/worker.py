"""Worker engine for Sherlock — executes jobs from a queue backend.

Phase 15 provides a local worker that can run safe mock scan jobs using the
Phase 5 scanner engine's MockTargetAdapter only. It does not scan external
targets, require real Redis or Supabase, or use real secrets.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from .jobs import JobPayload, JobResult, JobStatus, JobType, _utc_now_iso
from .queue import LocalMemoryQueue, QueueBackend
from .safety import SafetyGateResult, check_safety_gates


DEFAULT_OUTPUT_DIR = "worker-output"


@dataclass
class WorkerConfig:
    """Configuration for the worker engine."""
    output_dir: str = DEFAULT_OUTPUT_DIR
    max_concurrent_jobs: int = 1
    job_timeout_seconds: int = 300
    dry_run: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_dir": self.output_dir,
            "max_concurrent_jobs": self.max_concurrent_jobs,
            "job_timeout_seconds": self.job_timeout_seconds,
            "dry_run": self.dry_run,
        }


class WorkerEngine:
    """Processes jobs from a queue backend.

    Phase 15 supports local/mock execution only. The worker:
    - validates job payloads against safety gates
    - runs safe mock scans using Phase 5 scanner MockTargetAdapter
    - writes results to an ignored local output folder
    - does not scan external targets
    - does not require Redis, Supabase, or real secrets
    """

    def __init__(
        self,
        queue: QueueBackend | None = None,
        config: WorkerConfig | None = None,
    ) -> None:
        self.queue = queue or LocalMemoryQueue()
        self.config = config or WorkerConfig()

    def process_next(self) -> Optional[JobResult]:
        """Dequeue and process the next job. Return the result or None if empty."""
        payload = self.queue.dequeue()
        if payload is None:
            return None
        return self.execute(payload)

    def execute(self, payload: JobPayload) -> JobResult:
        """Execute a single job payload after safety gate checks."""
        started_at = _utc_now_iso()
        started = time.perf_counter()

        # Safety gate checks — skip queue_enabled for local dry-runs
        gate_result = check_safety_gates(payload, skip_queue_enabled_check=self.config.dry_run)
        if not gate_result.passed:
            result = self._blocked_result(payload, gate_result, started_at, started)
            self.queue.store_result(result)
            return result

        # Dispatch based on job type
        if payload.job_type == JobType.SCAN_RUN:
            result = self._execute_scan_run(payload, started_at, started)
        elif payload.job_type == JobType.SCAN_EVALUATE:
            result = self._execute_scan_evaluate(payload, started_at, started)
        elif payload.job_type == JobType.SCAN_SUMMARIZE:
            result = self._execute_scan_summarize(payload, started_at, started)
        elif payload.job_type == JobType.REPORT_PREPARE_PLACEHOLDER:
            result = self._execute_report_placeholder(payload, started_at, started)
        else:
            result = JobResult(
                job_id=payload.job_id,
                status=JobStatus.FAILED,
                started_at=started_at,
                completed_at=_utc_now_iso(),
                duration_ms=int((time.perf_counter() - started) * 1000),
                error_code="unknown_job_type",
                error_message=f"Unrecognized job type: {payload.job_type}",
            )

        self.queue.store_result(result)
        return result

    # ------------------------------------------------------------------
    # Job type handlers
    # ------------------------------------------------------------------

    def _execute_scan_run(
        self, payload: JobPayload, started_at: str, started: float
    ) -> JobResult:
        """Run a safe mock scan using Phase 5 scanner engine."""
        try:
            from packages.scanner_engine.config import ScanConfig, TargetConfig
            from packages.scanner_engine.runner import ScannerEngine
            from packages.scanner_engine.adapters import MockTargetAdapter

            target_snapshot = payload.target_snapshot or {}
            target_config = TargetConfig(
                name=target_snapshot.get("name", "Worker Mock Target"),
                type="mock",
                endpoint_url=None,
                method="POST",
                notes="Phase 15 worker mock scan — no network requests",
            )
            max_tests = min(
                payload.limits.get("max_tests", 3),
                10,  # Phase 5 scanner hard limit
            )
            scan_config = ScanConfig(
                target=target_config,
                scan_mode="safe_smoke",
                max_tests=max_tests,
                timeout_seconds=min(payload.limits.get("timeout_seconds", 10), 60),
                output_dir=self.config.output_dir,
                notes=f"Phase 15 worker job {payload.job_id}",
            )
            engine = ScannerEngine(scan_config, adapter=MockTargetAdapter(target_config, scan_config.timeout_seconds))
            scan_run = engine.run()

            completed_at = _utc_now_iso()
            duration_ms = int((time.perf_counter() - started) * 1000)
            summary = scan_run.to_summary()
            output_ref = summary.get("output_file_path", "")

            return JobResult(
                job_id=payload.job_id,
                status=JobStatus.COMPLETED if scan_run.session.state == "completed" else JobStatus.FAILED,
                started_at=started_at,
                completed_at=completed_at,
                duration_ms=duration_ms,
                output_reference=output_ref,
                summary=summary,
                safety_decision="mock_scan_only",
                metadata={
                    "scan_id": scan_run.session.scan_id,
                    "adapter": "mock",
                    "network_used": False,
                    "phase": "phase_15_worker_foundation",
                },
            )
        except Exception as error:
            return JobResult(
                job_id=payload.job_id,
                status=JobStatus.FAILED,
                started_at=started_at,
                completed_at=_utc_now_iso(),
                duration_ms=int((time.perf_counter() - started) * 1000),
                error_code="scan_run_error",
                error_message=str(error),
                safety_decision="error_before_execution",
            )

    def _execute_scan_evaluate(
        self, payload: JobPayload, started_at: str, started: float
    ) -> JobResult:
        """Placeholder for scan evaluation job. Not active in Phase 15."""
        return JobResult(
            job_id=payload.job_id,
            status=JobStatus.COMPLETED,
            started_at=started_at,
            completed_at=_utc_now_iso(),
            duration_ms=int((time.perf_counter() - started) * 1000),
            summary={"message": "scan.evaluate placeholder — evaluator integration is future work"},
            safety_decision="placeholder_only",
            metadata={"phase": "phase_15_worker_foundation"},
        )

    def _execute_scan_summarize(
        self, payload: JobPayload, started_at: str, started: float
    ) -> JobResult:
        """Placeholder for scan summarization job. Not active in Phase 15."""
        return JobResult(
            job_id=payload.job_id,
            status=JobStatus.COMPLETED,
            started_at=started_at,
            completed_at=_utc_now_iso(),
            duration_ms=int((time.perf_counter() - started) * 1000),
            summary={"message": "scan.summarize placeholder — summarization is future work"},
            safety_decision="placeholder_only",
            metadata={"phase": "phase_15_worker_foundation"},
        )

    def _execute_report_placeholder(
        self, payload: JobPayload, started_at: str, started: float
    ) -> JobResult:
        """Placeholder for report preparation job. Not active in Phase 15."""
        return JobResult(
            job_id=payload.job_id,
            status=JobStatus.COMPLETED,
            started_at=started_at,
            completed_at=_utc_now_iso(),
            duration_ms=int((time.perf_counter() - started) * 1000),
            summary={"message": "report.prepare_placeholder — report generation is future work"},
            safety_decision="placeholder_only",
            metadata={"phase": "phase_15_worker_foundation"},
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _blocked_result(
        self,
        payload: JobPayload,
        gate_result: SafetyGateResult,
        started_at: str,
        started: float,
    ) -> JobResult:
        """Build a blocked JobResult from a failed safety gate check."""
        if "target_verified" in gate_result.blocked_reason.lower() or "verification" in gate_result.blocked_reason.lower():
            status = JobStatus.BLOCKED_UNVERIFIED
        else:
            status = JobStatus.BLOCKED_UNSAFE
        return JobResult(
            job_id=payload.job_id,
            status=status,
            started_at=started_at,
            completed_at=_utc_now_iso(),
            duration_ms=int((time.perf_counter() - started) * 1000),
            error_code="safety_gate_blocked",
            error_message=gate_result.blocked_reason,
            safety_decision=f"blocked_by_gate",
            metadata={"gate_results": gate_result.gate_results},
        )


def write_worker_result(result: JobResult, output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
    """Write a job result to the local output folder. Return the file path."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_id = "".join(c if c.isalnum() or c in {"-", "_"} else "_" for c in result.job_id)
    path = out_dir / f"job-{safe_id}-result.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2, sort_keys=True)
        f.write("\n")
    return str(path)
