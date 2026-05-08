"""Job payload, result, and lifecycle definitions for Sherlock worker system.

All payloads must be JSON-serializable. Do not include secrets, API keys,
bearer tokens, cookies, passwords, private keys, raw headers, or production
credentials in job payloads.
"""
from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Job types
# ---------------------------------------------------------------------------

class JobType:
    SCAN_RUN = "scan.run"
    SCAN_EVALUATE = "scan.evaluate"
    SCAN_SUMMARIZE = "scan.summarize"
    REPORT_PREPARE_PLACEHOLDER = "report.prepare_placeholder"

    ALL: frozenset[str] = frozenset({
        "scan.run",
        "scan.evaluate",
        "scan.summarize",
        "report.prepare_placeholder",
    })


# ---------------------------------------------------------------------------
# Job lifecycle states
# ---------------------------------------------------------------------------

class JobStatus:
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"
    BLOCKED_UNVERIFIED = "blocked_unverified"
    BLOCKED_UNSAFE = "blocked_unsafe"

    ALL: frozenset[str] = frozenset({
        "queued",
        "running",
        "completed",
        "failed",
        "cancelled",
        "timed_out",
        "blocked_unverified",
        "blocked_unsafe",
    })

    TERMINAL: frozenset[str] = frozenset({
        "completed",
        "failed",
        "cancelled",
        "timed_out",
        "blocked_unverified",
        "blocked_unsafe",
    })

    ALLOWED_TRANSITIONS: Dict[str, frozenset[str]] = {
        "queued": frozenset({"running", "cancelled", "blocked_unverified", "blocked_unsafe"}),
        "running": frozenset({"completed", "failed", "cancelled", "timed_out"}),
    }


def is_valid_transition(current: str, target: str) -> bool:
    """Return True if transitioning from *current* to *target* is allowed."""
    allowed = JobStatus.ALLOWED_TRANSITIONS.get(current, frozenset())
    return target in allowed


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# Patterns that look like secrets — used by safety gates
SECRET_FIELD_PATTERNS: List[str] = [
    r"api_key",
    r"api_secret",
    r"bearer_token",
    r"access_token",
    r"refresh_token",
    r"password",
    r"passwd",
    r"private_key",
    r"secret_key",
    r"cookie",
    r"session_token",
    r"x_api_key",
    r"authorization_header",
    r"raw_header",
    r"credential",
]

_SECRET_REGEX = re.compile(
    r"(?i)(" + "|".join(SECRET_FIELD_PATTERNS) + r")",
)


def contains_secret_looking_fields(data: Dict[str, Any], path: str = "") -> List[str]:
    """Recursively inspect *data* keys for secret-looking names. Return a list of flagged paths."""
    flagged: List[str] = []
    for key, value in data.items():
        full_path = f"{path}.{key}" if path else key
        if _SECRET_REGEX.search(key):
            flagged.append(full_path)
        if isinstance(value, dict):
            flagged.extend(contains_secret_looking_fields(value, full_path))
    return flagged


# ---------------------------------------------------------------------------
# Job payload
# ---------------------------------------------------------------------------

DEFAULT_SCAN_MAX_TESTS = 25


@dataclass
class JobPayload:
    """JSON-serializable job payload.

    Do NOT include secrets, raw API keys, bearer tokens, cookies,
    passwords, private keys, raw headers, or production credentials.
    """
    job_id: str
    job_type: str
    project_id: str = ""
    target_id: str = ""
    scan_id: str = ""
    organization_id: str = ""
    requested_by_user_id: str = ""
    scan_type: str = "safe_smoke"
    verification_status: str = "unverified"
    target_snapshot: Dict[str, Any] = field(default_factory=dict)
    limits: Dict[str, Any] = field(default_factory=lambda: {
        "max_tests": DEFAULT_SCAN_MAX_TESTS,
        "timeout_seconds": 300,
    })
    created_at: str = field(default_factory=_utc_now_iso)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "job_type": self.job_type,
            "project_id": self.project_id,
            "target_id": self.target_id,
            "scan_id": self.scan_id,
            "organization_id": self.organization_id,
            "requested_by_user_id": self.requested_by_user_id,
            "scan_type": self.scan_type,
            "verification_status": self.verification_status,
            "target_snapshot": self.target_snapshot,
            "limits": self.limits,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobPayload":
        return cls(
            job_id=data.get("job_id", ""),
            job_type=data.get("job_type", ""),
            project_id=data.get("project_id", ""),
            target_id=data.get("target_id", ""),
            scan_id=data.get("scan_id", ""),
            organization_id=data.get("organization_id", ""),
            requested_by_user_id=data.get("requested_by_user_id", ""),
            scan_type=data.get("scan_type", "safe_smoke"),
            verification_status=data.get("verification_status", "unverified"),
            target_snapshot=data.get("target_snapshot", {}),
            limits=data.get("limits", {"max_tests": DEFAULT_SCAN_MAX_TESTS, "timeout_seconds": 300}),
            created_at=data.get("created_at", _utc_now_iso()),
            metadata=data.get("metadata", {}),
        )


def create_job_payload(
    job_type: str,
    *,
    project_id: str = "",
    target_id: str = "",
    scan_id: str = "",
    organization_id: str = "",
    requested_by_user_id: str = "",
    scan_type: str = "safe_smoke",
    verification_status: str = "unverified",
    target_snapshot: Optional[Dict[str, Any]] = None,
    limits: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> JobPayload:
    """Factory for creating a new job payload with a generated UUID job_id."""
    return JobPayload(
        job_id=str(uuid.uuid4()),
        job_type=job_type,
        project_id=project_id,
        target_id=target_id,
        scan_id=scan_id,
        organization_id=organization_id,
        requested_by_user_id=requested_by_user_id,
        scan_type=scan_type,
        verification_status=verification_status,
        target_snapshot=target_snapshot or {},
        limits=limits or {"max_tests": DEFAULT_SCAN_MAX_TESTS, "timeout_seconds": 300},
        metadata=metadata or {},
    )


# ---------------------------------------------------------------------------
# Job result
# ---------------------------------------------------------------------------

@dataclass
class JobResult:
    """JSON-serializable worker result."""
    job_id: str
    status: str
    started_at: str = ""
    completed_at: str = ""
    duration_ms: int = 0
    output_reference: str = ""
    summary: Dict[str, Any] = field(default_factory=dict)
    error_code: str = ""
    error_message: str = ""
    safety_decision: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "output_reference": self.output_reference,
            "summary": self.summary,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "safety_decision": self.safety_decision,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobResult":
        return cls(
            job_id=data.get("job_id", ""),
            status=data.get("status", ""),
            started_at=data.get("started_at", ""),
            completed_at=data.get("completed_at", ""),
            duration_ms=data.get("duration_ms", 0),
            output_reference=data.get("output_reference", ""),
            summary=data.get("summary", {}),
            error_code=data.get("error_code", ""),
            error_message=data.get("error_message", ""),
            safety_decision=data.get("safety_decision", ""),
            metadata=data.get("metadata", {}),
        )
