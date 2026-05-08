"""Safety gate checks for Sherlock worker system.

These gates run before a job is dispatched to execution. If any gate
fails, the job should be blocked rather than executed.

Phase 15 implements conceptual and code-level helpers. No aggressive
network checks, SSRF hardening, or production enforcement exists yet.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .jobs import DEFAULT_SCAN_MAX_TESTS, JobPayload, JobType, contains_secret_looking_fields


# ---------------------------------------------------------------------------
# Safety gate result
# ---------------------------------------------------------------------------

@dataclass
class SafetyGateResult:
    """Aggregated result of all safety gate checks."""
    passed: bool
    blocked_reason: str = ""
    gate_results: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "blocked_reason": self.blocked_reason,
            "gate_results": self.gate_results,
        }


# ---------------------------------------------------------------------------
# Individual gate checks
# ---------------------------------------------------------------------------

def _gate_result(name: str, passed: bool, reason: str = "") -> Dict[str, Any]:
    return {"gate": name, "passed": passed, "reason": reason}


def _check_queue_enabled() -> Dict[str, Any]:
    """Block if the queue/worker is disabled in the environment."""
    enabled = os.getenv("WORKER_ENABLED", "false").strip().lower() in {"1", "true", "yes", "on"}
    if not enabled:
        return _gate_result("queue_enabled", False, "WORKER_ENABLED is not set to true in the current environment.")
    return _gate_result("queue_enabled", True)


def _check_target_verified(payload: JobPayload) -> Dict[str, Any]:
    """Block if the target has not passed ownership verification."""
    if payload.verification_status != "verified":
        return _gate_result(
            "target_verified",
            False,
            f"Target verification status is '{payload.verification_status}'; must be 'verified' before scan jobs can run.",
        )
    return _gate_result("target_verified", True)


def _check_job_type_allowed(payload: JobPayload) -> Dict[str, Any]:
    """Block if the job type is not in the allowed set."""
    if payload.job_type not in JobType.ALL:
        return _gate_result(
            "job_type_allowed",
            False,
            f"Job type '{payload.job_type}' is not recognized. Allowed: {sorted(JobType.ALL)}",
        )
    return _gate_result("job_type_allowed", True)


_UNSAFE_URL_PATTERN = re.compile(
    r"(?i)^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|169\.254\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+|metadata\.google|metadata\.aws)",
)


def _check_target_url_safe(payload: JobPayload) -> Dict[str, Any]:
    """Block if the target snapshot URL is missing or points to a private/internal address.

    This is a basic check. Full SSRF hardening is Phase 22.
    """
    url = payload.target_snapshot.get("endpoint_url", "")
    if not url or not isinstance(url, str):
        # Mock targets may not have a URL — only block if scan_type requires one
        if payload.scan_type != "safe_smoke":
            return _gate_result("target_url_safe", False, "Target snapshot is missing endpoint_url for non-mock scan type.")
        return _gate_result("target_url_safe", True, "No endpoint_url required for safe_smoke scan type.")
    if _UNSAFE_URL_PATTERN.match(url):
        return _gate_result("target_url_safe", False, f"Target URL '{url}' points to a private/internal address and is blocked.")
    return _gate_result("target_url_safe", True)


def _check_no_secrets_in_payload(payload: JobPayload) -> Dict[str, Any]:
    """Block if the job payload contains fields that look like secrets."""
    flagged: List[str] = []
    flagged.extend(contains_secret_looking_fields(payload.target_snapshot, "target_snapshot"))
    flagged.extend(contains_secret_looking_fields(payload.metadata, "metadata"))
    if flagged:
        return _gate_result(
            "no_secrets_in_payload",
            False,
            f"Job payload contains secret-looking fields: {', '.join(flagged)}. Remove secrets from job payloads.",
        )
    return _gate_result("no_secrets_in_payload", True)


def _check_limits(payload: JobPayload) -> Dict[str, Any]:
    """Block if requested limits exceed configured maximums."""
    max_tests_env = os.getenv("SCAN_MAX_TESTS_PER_JOB", str(DEFAULT_SCAN_MAX_TESTS))
    try:
        configured_max = int(max_tests_env)
    except ValueError:
        configured_max = DEFAULT_SCAN_MAX_TESTS

    requested_max = payload.limits.get("max_tests", DEFAULT_SCAN_MAX_TESTS)
    if not isinstance(requested_max, int) or requested_max < 1:
        return _gate_result("limits", False, "limits.max_tests must be a positive integer.")
    if requested_max > configured_max:
        return _gate_result(
            "limits",
            False,
            f"Requested max_tests ({requested_max}) exceeds configured maximum ({configured_max}).",
        )

    timeout = payload.limits.get("timeout_seconds", 300)
    max_timeout = int(os.getenv("WORKER_JOB_TIMEOUT_SECONDS", "300"))
    if not isinstance(timeout, int) or timeout < 1:
        return _gate_result("limits", False, "limits.timeout_seconds must be a positive integer.")
    if timeout > max_timeout:
        return _gate_result(
            "limits",
            False,
            f"Requested timeout ({timeout}s) exceeds configured maximum ({max_timeout}s).",
        )

    return _gate_result("limits", True)


# ---------------------------------------------------------------------------
# Aggregate gate check
# ---------------------------------------------------------------------------

def check_safety_gates(
    payload: JobPayload,
    *,
    skip_queue_enabled_check: bool = False,
) -> SafetyGateResult:
    """Run all safety gates against *payload* and return the aggregate result.

    Set *skip_queue_enabled_check* to True for local/dev dry-runs where
    WORKER_ENABLED may not be set.
    """
    results: List[Dict[str, Any]] = []

    if not skip_queue_enabled_check:
        results.append(_check_queue_enabled())
    results.append(_check_target_verified(payload))
    results.append(_check_job_type_allowed(payload))
    results.append(_check_target_url_safe(payload))
    results.append(_check_no_secrets_in_payload(payload))
    results.append(_check_limits(payload))

    failed = [r for r in results if not r["passed"]]
    if failed:
        first_failure = failed[0]
        return SafetyGateResult(
            passed=False,
            blocked_reason=first_failure["reason"],
            gate_results=results,
        )
    return SafetyGateResult(passed=True, gate_results=results)
