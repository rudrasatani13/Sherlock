"""Structured finding models for the Phase 17 findings system."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

from .categories import category_display_name, normalize_category
from .evidence import EvidenceItem, evidence_summary, redact_evidence_text, summarize_evidence
from .severity import (
    SEVERITY_CRITICAL,
    SEVERITY_HIGH,
    normalize_confidence,
    normalize_severity,
)
from .statuses import STATUS_FALSE_POSITIVE, normalize_status


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class FindingValidationError(ValueError):
    """Raised when a finalized finding violates the Phase 17 contract."""


@dataclass
class FindingCandidate:
    """A lightweight evaluator-derived observation that may need review."""

    category: str
    detector_name: str
    severity_hint: str
    confidence_hint: str
    observed_behavior: str
    evidence_snippet: str = ""
    redacted_evidence: str = ""
    test_case_id: str = ""
    needs_manual_review: bool = False
    reason: str = ""
    affected_target: str = ""
    source_scan_id: str = ""
    source_test_ids: List[str] = field(default_factory=list)
    evaluator_signals: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.category = normalize_category(self.category)
        self.severity_hint = normalize_severity(self.severity_hint)
        self.confidence_hint = normalize_confidence(self.confidence_hint)
        self.detector_name = (self.detector_name or "evaluator_signal").strip()
        self.observed_behavior = _clean_text(self.observed_behavior)
        safe_evidence = redact_evidence_text(self.redacted_evidence or self.evidence_snippet)
        self.evidence_snippet = summarize_evidence(safe_evidence)
        self.redacted_evidence = summarize_evidence(safe_evidence)
        if self.test_case_id and self.test_case_id not in self.source_test_ids:
            self.source_test_ids.append(self.test_case_id)
        self.source_test_ids = _unique_strings(self.source_test_ids)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "detector_name": self.detector_name,
            "severity_hint": self.severity_hint,
            "confidence_hint": self.confidence_hint,
            "observed_behavior": self.observed_behavior,
            "evidence_snippet": self.evidence_snippet,
            "redacted_evidence": self.redacted_evidence,
            "test_case_id": self.test_case_id,
            "needs_manual_review": self.needs_manual_review,
            "reason": self.reason,
            "affected_target": self.affected_target,
            "source_scan_id": self.source_scan_id,
            "source_test_ids": list(self.source_test_ids),
            "evaluator_signals": list(self.evaluator_signals),
            "metadata": dict(self.metadata),
        }


@dataclass
class Finding:
    """A validated, report-ready finding object.

    This object is not persisted by Phase 17. It is a reusable internal
    structure for future reviewed findings and Phase 18 web reports.
    """

    finding_id: str
    title: str
    category: str
    severity: str
    confidence: str
    status: str
    description: str
    business_impact: str
    evidence_summary: str
    evidence_items: List[EvidenceItem] = field(default_factory=list)
    reproduction_steps: List[str] = field(default_factory=list)
    fix_recommendation: str = ""
    affected_target: str = ""
    source_scan_id: str = ""
    source_test_ids: List[str] = field(default_factory=list)
    evaluator_signals: List[Dict[str, Any]] = field(default_factory=list)
    duplicate_group_key: str = ""
    manual_review_required: bool = False
    manual_review_notes: str = ""
    accepted_risk_reason: str = ""
    false_positive_reason: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.title = _clean_text(self.title)
        self.category = normalize_category(self.category)
        self.severity = normalize_severity(self.severity)
        self.confidence = normalize_confidence(self.confidence)
        self.status = normalize_status(self.status)
        self.description = _clean_text(self.description)
        self.business_impact = _clean_text(self.business_impact)
        self.fix_recommendation = _clean_text(self.fix_recommendation)
        self.accepted_risk_reason = _clean_text(self.accepted_risk_reason)
        self.evidence_items = [
            EvidenceItem(
                signal=item.signal,
                summary=summarize_evidence(item.summary),
                redacted_snippet=summarize_evidence(item.redacted_snippet or item.summary),
                source_test_id=item.source_test_id,
                strong_evidence=item.strong_evidence,
            )
            for item in self.evidence_items
        ]
        self.evidence_summary = evidence_summary(self.evidence_items, self.evidence_summary)
        self.reproduction_steps = [_clean_text(step) for step in self.reproduction_steps if _clean_text(step)]
        self.source_test_ids = _unique_strings(self.source_test_ids)
        if not self.finding_id:
            self.finding_id = stable_finding_id(
                self.title,
                self.category,
                self.affected_target,
                ",".join(self.source_test_ids),
            )
        if not self.duplicate_group_key:
            self.duplicate_group_key = stable_group_seed(self.category, self.affected_target, self.title)
        self.ensure_valid()

    @property
    def has_strong_evidence(self) -> bool:
        if bool(self.metadata.get("strong_evidence")):
            return True
        return any(item.strong_evidence for item in self.evidence_items)

    def ensure_valid(self) -> None:
        errors = validate_finding(self)
        if errors:
            raise FindingValidationError("; ".join(errors))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "title": self.title,
            "category": self.category,
            "severity": self.severity,
            "confidence": self.confidence,
            "status": self.status,
            "description": self.description,
            "business_impact": self.business_impact,
            "evidence_summary": self.evidence_summary,
            "evidence_items": [item.to_dict() for item in self.evidence_items],
            "reproduction_steps": list(self.reproduction_steps),
            "fix_recommendation": self.fix_recommendation,
            "affected_target": self.affected_target,
            "source_scan_id": self.source_scan_id,
            "source_test_ids": list(self.source_test_ids),
            "evaluator_signals": list(self.evaluator_signals),
            "duplicate_group_key": self.duplicate_group_key,
            "manual_review_required": self.manual_review_required,
            "manual_review_notes": self.manual_review_notes,
            "accepted_risk_reason": self.accepted_risk_reason,
            "false_positive_reason": self.false_positive_reason,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }


def validate_finding(finding: Finding) -> List[str]:
    """Return validation errors for a finalized finding."""
    errors: List[str] = []
    if not finding.title:
        errors.append("finding title is required")
    if _is_vague(finding.title):
        errors.append("finding title is too vague")
    if not finding.description or _is_vague(finding.description):
        errors.append("finding description must be plain-English and specific")
    if not finding.business_impact:
        errors.append("business impact is required")
    if finding.severity in {SEVERITY_CRITICAL, SEVERITY_HIGH}:
        if not finding.evidence_summary:
            errors.append("critical/high findings require an evidence summary")
        if not finding.fix_recommendation:
            errors.append("critical/high findings require a fix recommendation")
        if not (finding.has_strong_evidence or finding.manual_review_required):
            errors.append("critical/high findings require strong evidence or manual review")
    if finding.severity == SEVERITY_CRITICAL and not (finding.has_strong_evidence or finding.manual_review_required):
        errors.append("critical findings require strong evidence or manual review")
    if finding.status == STATUS_FALSE_POSITIVE and not finding.false_positive_reason:
        errors.append("false_positive findings require a reason")
    return errors


def stable_finding_id(*parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"shk_find_{digest}"


def stable_group_seed(category: str, affected_target: str, title: str) -> str:
    seed = "|".join((normalize_category(category), _slug(affected_target), _slug(title)))
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def display_title_for_category(category: str, detector_name: str = "") -> str:
    name = category_display_name(category)
    detector = (detector_name or "").replace("_", " ").strip()
    if detector:
        return f"{name}: {detector}"
    return f"{name} finding requires review"


def _clean_text(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def _unique_strings(values: List[str]) -> List[str]:
    unique: List[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in unique:
            unique.append(text)
    return unique


def _slug(value: str | None) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in (value or "")).strip("_")


def _is_vague(value: str) -> bool:
    normalized = _clean_text(value).lower()
    if len(normalized.split()) < 3:
        return True
    return normalized in {
        "security issue found",
        "vulnerability found",
        "bad output",
        "issue found",
        "needs review",
    }
