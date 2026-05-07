from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


SCAN_STATES = ("pending", "running", "completed", "failed")
TEST_STATUSES = ("pending", "completed", "failed")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class ScannerTest:
    test_id: str
    category: str
    input: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "category": self.category,
            "input": self.input,
            "metadata": self.metadata,
        }


@dataclass
class TargetResponse:
    status_code: Optional[int]
    body: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "body": self.body,
            "metadata": self.metadata,
        }


@dataclass
class TestResult:
    test_id: str
    category: str
    input: str
    response: Optional[TargetResponse]
    status: str
    error: Optional[str]
    started_at: str
    completed_at: str
    duration_ms: int
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "category": self.category,
            "input": self.input,
            "response": self.response.to_dict() if self.response else None,
            "status": self.status,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
        }


@dataclass
class ScanSession:
    scan_id: str
    target_name: str
    target_type: str
    mode: str
    state: str = "pending"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scan_id": self.scan_id,
            "target_name": self.target_name,
            "target_type": self.target_type,
            "mode": self.mode,
            "state": self.state,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
        }


@dataclass
class ScanRun:
    session: ScanSession
    target: Dict[str, Any]
    tests: List[ScannerTest]
    results: List[TestResult] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)

    def completed_count(self) -> int:
        return sum(1 for result in self.results if result.status == "completed")

    def failed_count(self) -> int:
        return sum(1 for result in self.results if result.status == "failed")

    def to_raw_results(self) -> Dict[str, Any]:
        return {
            "scan_id": self.session.scan_id,
            "results": [result.to_dict() for result in self.results],
        }

    def to_structured_result(self) -> Dict[str, Any]:
        return {
            "schema": "powerdetect-sherlock-scan-result-v0",
            "scan": self.session.to_dict(),
            "target": self.target,
            "tests": [test.to_dict() for test in self.tests],
            "results": [result.to_dict() for result in self.results],
            "extension_points": {
                "prompt_library": "available_in_phase_6_not_executed_by_default",
                "evaluator_system": "not_implemented_until_phase_7",
                "backend_api": "not_implemented_in_phase_5",
                "report_generator": "not_implemented_in_phase_5",
            },
        }

    def to_summary(self) -> Dict[str, Any]:
        return {
            "schema": "powerdetect-sherlock-scan-summary-v0",
            "scan_id": self.session.scan_id,
            "target_name": self.session.target_name,
            "target_type": self.session.target_type,
            "state": self.session.state,
            "total_tests": len(self.tests),
            "completed_tests": self.completed_count(),
            "failed_tests": self.failed_count(),
            "started_at": self.session.started_at,
            "completed_at": self.session.completed_at,
            "output_file_path": self.output_paths.get("structured_result"),
            "raw_results_file_path": self.output_paths.get("raw_results"),
            "summary_file_path": self.output_paths.get("summary"),
        }
