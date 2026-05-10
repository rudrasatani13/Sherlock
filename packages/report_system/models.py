"""Report data models for the Phase 18 web report foundation."""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


REPORT_STATUS_DRAFT = "draft"
REPORT_STATUS_READY = "ready"
REPORT_STATUS_NEEDS_REVIEW = "needs_review"
REPORT_STATUS_ARCHIVED = "archived"

REPORT_STATUSES: tuple[str, ...] = (
    REPORT_STATUS_DRAFT,
    REPORT_STATUS_READY,
    REPORT_STATUS_NEEDS_REVIEW,
    REPORT_STATUS_ARCHIVED,
)

REPORT_TYPE_WEB = "web"
REPORT_TYPE_SAMPLE = "sample"
REPORT_TYPE_MANUAL_AUDIT = "manual_audit"
REPORT_TYPE_SCAN_SUMMARY = "scan_summary"

REPORT_TYPES: tuple[str, ...] = (
    REPORT_TYPE_WEB,
    REPORT_TYPE_SAMPLE,
    REPORT_TYPE_MANUAL_AUDIT,
    REPORT_TYPE_SCAN_SUMMARY,
)

VERDICT_READY_WITH_LOW_RISK = "ready_with_low_risk"
VERDICT_NEEDS_FIXES_BEFORE_LAUNCH = "needs_fixes_before_launch"
VERDICT_HIGH_RISK_DO_NOT_LAUNCH = "high_risk_do_not_launch"
VERDICT_MANUAL_REVIEW_REQUIRED = "manual_review_required"
VERDICT_INCONCLUSIVE = "inconclusive"

LAUNCH_READINESS_VERDICTS: tuple[str, ...] = (
    VERDICT_READY_WITH_LOW_RISK,
    VERDICT_NEEDS_FIXES_BEFORE_LAUNCH,
    VERDICT_HIGH_RISK_DO_NOT_LAUNCH,
    VERDICT_MANUAL_REVIEW_REQUIRED,
    VERDICT_INCONCLUSIVE,
)

REPORT_SYSTEM_VERSION = "phase_18_report_system_v0.1"
METHODOLOGY_VERSION = "phase_3_methodology"
FINDINGS_SYSTEM_VERSION = "phase_17_findings_system"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_report_status(value: str | None) -> str:
    normalized = (value or REPORT_STATUS_DRAFT).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in REPORT_STATUSES:
        raise ValueError(f"unsupported report status: {value}")
    return normalized


def normalize_report_type(value: str | None) -> str:
    normalized = (value or REPORT_TYPE_SAMPLE).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in REPORT_TYPES:
        raise ValueError(f"unsupported report type: {value}")
    return normalized


def normalize_launch_readiness_verdict(value: str | None) -> str:
    normalized = (value or VERDICT_INCONCLUSIVE).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in LAUNCH_READINESS_VERDICTS:
        raise ValueError(f"unsupported launch readiness verdict: {value}")
    return normalized


@dataclass
class SeverityBreakdown:
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    informational: int = 0

    @property
    def total(self) -> int:
        return self.critical + self.high + self.medium + self.low + self.informational

    def to_dict(self) -> Dict[str, int]:
        return {
            "critical": self.critical,
            "high": self.high,
            "medium": self.medium,
            "low": self.low,
            "informational": self.informational,
            "total": self.total,
        }


@dataclass
class SecurityScore:
    score: int
    max_score: int = 100
    rating: str = ""
    explanation: str = ""
    limitations: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0 <= int(self.score) <= self.max_score:
            raise ValueError("security score must be between 0 and max_score")
        self.score = int(self.score)
        if not self.rating:
            self.rating = score_rating(self.score)
        self.limitations = _clean_list(self.limitations)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LaunchReadinessVerdict:
    verdict: str
    label: str
    summary: str
    recommended_action: str

    def __post_init__(self) -> None:
        self.verdict = normalize_launch_readiness_verdict(self.verdict)
        self.label = _clean_text(self.label)
        self.summary = _clean_text(self.summary)
        self.recommended_action = _clean_text(self.recommended_action)
        forbidden = ("secure", "safe", "certified", "guaranteed")
        combined = f"{self.verdict} {self.label} {self.summary} {self.recommended_action}".lower()
        if any(word in combined for word in forbidden):
            raise ValueError("launch readiness verdict must not use overclaiming language")

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class EvidenceSnippet:
    signal: str
    summary: str
    redacted_snippet: str
    source_test_id: str = ""

    def __post_init__(self) -> None:
        self.signal = _clean_text(self.signal or "evidence")
        self.summary = _clean_text(self.summary)
        self.redacted_snippet = _clean_text(self.redacted_snippet)
        self.source_test_id = _clean_text(self.source_test_id)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class ReportFinding:
    finding_id: str
    title: str
    category: str
    category_display_name: str
    severity: str
    confidence: str
    status: str
    description: str
    business_impact: str
    business_impact_summary: str
    evidence_summary: str
    evidence_items: List[EvidenceSnippet] = field(default_factory=list)
    reproduction_steps: List[str] = field(default_factory=list)
    fix_recommendation: str = ""
    fix_recommendation_summary: str = ""
    manual_review_note: str = ""
    limitations: List[str] = field(default_factory=list)
    source_test_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.finding_id = _clean_text(self.finding_id) or stable_report_id(self.title, self.category)
        self.title = _clean_text(self.title)
        self.category = _clean_text(self.category)
        self.category_display_name = _clean_text(self.category_display_name)
        self.severity = _clean_text(self.severity)
        self.confidence = _clean_text(self.confidence)
        self.status = _clean_text(self.status)
        self.description = _clean_text(self.description)
        self.business_impact = _clean_text(self.business_impact)
        self.business_impact_summary = _clean_text(self.business_impact_summary)
        self.evidence_summary = _clean_text(self.evidence_summary)
        self.reproduction_steps = _clean_list(self.reproduction_steps)
        self.fix_recommendation = _clean_text(self.fix_recommendation)
        self.fix_recommendation_summary = _clean_text(self.fix_recommendation_summary)
        self.manual_review_note = _clean_text(self.manual_review_note)
        self.limitations = _clean_list(self.limitations)
        self.source_test_ids = _clean_list(self.source_test_ids)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["evidence_items"] = [item.to_dict() for item in self.evidence_items]
        return data


@dataclass
class TopFix:
    title: str
    severity: str
    confidence: str
    category: str
    finding_ids: List[str]
    recommendation: str
    business_impact_summary: str = ""

    def __post_init__(self) -> None:
        self.title = _clean_text(self.title)
        self.severity = _clean_text(self.severity)
        self.confidence = _clean_text(self.confidence)
        self.category = _clean_text(self.category)
        self.finding_ids = _clean_list(self.finding_ids)
        self.recommendation = _clean_text(self.recommendation)
        self.business_impact_summary = _clean_text(self.business_impact_summary)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TestedCategory:
    category: str
    display_name: str
    status: str = "tested"
    notes: str = ""

    def __post_init__(self) -> None:
        self.category = _clean_text(self.category)
        self.display_name = _clean_text(self.display_name)
        self.status = _clean_text(self.status or "tested")
        self.notes = _clean_text(self.notes)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class Report:
    report_id: str
    report_type: str
    title: str
    project_name: str
    target_name: str
    scan_type: str
    report_status: str
    generated_at: str
    launch_readiness_verdict: LaunchReadinessVerdict
    security_score: SecurityScore
    executive_summary: str
    severity_breakdown: SeverityBreakdown
    top_fixes: List[TopFix]
    findings: List[ReportFinding]
    tested_categories: List[TestedCategory]
    not_tested: List[str]
    limitations: List[str]
    evidence_handling_note: str
    retest_status: str
    methodology_version: str = METHODOLOGY_VERSION
    findings_system_version: str = FINDINGS_SYSTEM_VERSION
    source_scan_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.report_type = normalize_report_type(self.report_type)
        self.report_status = normalize_report_status(self.report_status)
        self.report_id = _clean_text(self.report_id) or stable_report_id(
            self.title,
            self.project_name,
            self.target_name,
            self.generated_at,
        )
        self.title = _clean_text(self.title)
        self.project_name = _clean_text(self.project_name)
        self.target_name = _clean_text(self.target_name)
        self.scan_type = _clean_text(self.scan_type)
        self.executive_summary = _clean_text(self.executive_summary)
        self.not_tested = _clean_list(self.not_tested)
        self.limitations = _clean_list(self.limitations)
        self.evidence_handling_note = _clean_text(self.evidence_handling_note)
        self.retest_status = _clean_text(self.retest_status)
        self.methodology_version = _clean_text(self.methodology_version)
        self.findings_system_version = _clean_text(self.findings_system_version)
        self.source_scan_id = _clean_text(self.source_scan_id)
        if not self.limitations:
            raise ValueError("web reports must include limitations")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "report_type": self.report_type,
            "title": self.title,
            "project_name": self.project_name,
            "target_name": self.target_name,
            "scan_type": self.scan_type,
            "report_status": self.report_status,
            "generated_at": self.generated_at,
            "launch_readiness_verdict": self.launch_readiness_verdict.to_dict(),
            "security_score": self.security_score.to_dict(),
            "executive_summary": self.executive_summary,
            "severity_breakdown": self.severity_breakdown.to_dict(),
            "top_fixes": [item.to_dict() for item in self.top_fixes],
            "findings": [item.to_dict() for item in self.findings],
            "tested_categories": [item.to_dict() for item in self.tested_categories],
            "not_tested": list(self.not_tested),
            "limitations": list(self.limitations),
            "evidence_handling_note": self.evidence_handling_note,
            "retest_status": self.retest_status,
            "methodology_version": self.methodology_version,
            "findings_system_version": self.findings_system_version,
            "source_scan_id": self.source_scan_id,
            "metadata": _plain(self.metadata),
        }


def stable_report_id(*parts: str) -> str:
    digest = hashlib.sha256("|".join(str(part or "") for part in parts).encode("utf-8")).hexdigest()[:12]
    return f"shk_report_{digest}"


def score_rating(score: int) -> str:
    if score >= 85:
        return "low observed launch risk"
    if score >= 70:
        return "moderate observed launch risk"
    if score >= 50:
        return "material launch risk"
    return "high observed launch risk"


def _clean_text(value: str | None) -> str:
    return " ".join(str(value or "").strip().split())


def _clean_list(values: List[str] | tuple[str, ...] | None) -> List[str]:
    output: List[str] = []
    for value in values or []:
        text = _clean_text(str(value))
        if text and text not in output:
            output.append(text)
    return output


def _plain(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value
