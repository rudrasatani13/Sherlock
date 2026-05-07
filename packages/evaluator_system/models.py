from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .constants import (
    ALLOWED_CONFIDENCES,
    ALLOWED_SEVERITIES,
    ALLOWED_VERDICTS,
    CONFIDENCE_NONE,
    EVALUATOR_VERSION,
    SEVERITY_NONE,
    VERDICT_ERROR,
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class EvidenceSnippet:
    signal: str
    snippet: str
    redacted_snippet: str
    start: int
    end: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal": self.signal,
            "snippet": self.snippet,
            "redacted_snippet": self.redacted_snippet,
            "start": self.start,
            "end": self.end,
        }


@dataclass(frozen=True)
class MatchedSignal:
    name: str
    group: str
    severity: str
    confidence: str
    evidence_count: int
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "group": self.group,
            "severity": self.severity,
            "confidence": self.confidence,
            "evidence_count": self.evidence_count,
            "description": self.description,
        }


@dataclass(frozen=True)
class EvaluationInput:
    test_id: str
    category: str
    input: str
    response_body: str
    response_status_code: Optional[int]
    scan_status: str
    error: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    @classmethod
    def from_scan_result(cls, value: Dict[str, Any]) -> "EvaluationInput":
        response = value.get("response") or {}
        response_metadata = response.get("metadata") if isinstance(response, dict) else None
        metadata = dict(value.get("metadata") or {})
        if isinstance(response_metadata, dict) and response_metadata:
            metadata["response_metadata"] = response_metadata
        return cls(
            test_id=str(value.get("test_id") or "unknown_test"),
            category=str(value.get("category") or "unknown"),
            input=str(value.get("input") or ""),
            response_body=str(response.get("body") or "") if isinstance(response, dict) else "",
            response_status_code=response.get("status_code") if isinstance(response, dict) else None,
            scan_status=str(value.get("status") or "unknown"),
            error=value.get("error"),
            metadata=metadata,
            started_at=value.get("started_at"),
            completed_at=value.get("completed_at"),
        )


@dataclass(frozen=True)
class EvaluationResult:
    test_id: str
    category: str
    verdict: str
    severity: str
    confidence: str
    matched_signals: List[MatchedSignal]
    evidence: List[EvidenceSnippet]
    reasoning_summary: str
    needs_manual_review: bool
    manual_review_reasons: List[str]
    evaluator_version: str = EVALUATOR_VERSION
    evaluated_at: str = field(default_factory=utc_now_iso)
    error: Optional[str] = None

    def __post_init__(self) -> None:
        if self.verdict not in ALLOWED_VERDICTS:
            raise ValueError(f"unsupported verdict: {self.verdict}")
        if self.severity not in ALLOWED_SEVERITIES:
            raise ValueError(f"unsupported severity: {self.severity}")
        if self.confidence not in ALLOWED_CONFIDENCES:
            raise ValueError(f"unsupported confidence: {self.confidence}")

    @classmethod
    def error_result(cls, evaluation_input: EvaluationInput, message: str) -> "EvaluationResult":
        return cls(
            test_id=evaluation_input.test_id,
            category=evaluation_input.category,
            verdict=VERDICT_ERROR,
            severity=SEVERITY_NONE,
            confidence=CONFIDENCE_NONE,
            matched_signals=[],
            evidence=[],
            reasoning_summary="Evaluation could not be completed.",
            needs_manual_review=True,
            manual_review_reasons=[message],
            error=message,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "category": self.category,
            "verdict": self.verdict,
            "severity": self.severity,
            "confidence": self.confidence,
            "matched_signals": [signal.to_dict() for signal in self.matched_signals],
            "evidence": [item.to_dict() for item in self.evidence],
            "reasoning_summary": self.reasoning_summary,
            "needs_manual_review": self.needs_manual_review,
            "manual_review_reasons": list(self.manual_review_reasons),
            "evaluator_version": self.evaluator_version,
            "evaluated_at": self.evaluated_at,
            "error": self.error,
        }
