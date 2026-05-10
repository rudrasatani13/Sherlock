"""Section builders for Phase 18 web reports."""
from __future__ import annotations

import re
from typing import Any, Iterable, List

from packages.findings_system.categories import category_display_name, normalize_category
from packages.findings_system.severity import CONFIDENCE_RANK, SEVERITY_RANK, normalize_confidence, normalize_severity
from packages.findings_system.statuses import normalize_status

from .evidence import format_report_evidence_items, redacted_report_evidence_summary
from .models import ReportFinding, SeverityBreakdown, TestedCategory, TopFix


DEFAULT_LIMITATIONS: tuple[str, ...] = (
    "This report is not a guarantee of security and does not claim that all vulnerabilities were found.",
    "Only the listed categories, target surfaces, roles, data sources, tools, and assumptions were tested.",
    "Automated results and ambiguous evidence require human review before final launch decisions.",
    "Unavailable integrations, untested tools, hidden data sources, or changed model behavior may hide additional risks.",
    "No destructive testing is included unless it is explicitly authorized, scoped, and isolated.",
    "The current Phase 18 web report shell uses sanitized static demo data only and is not generated from a real customer scan.",
)

EVIDENCE_HANDLING_NOTE = (
    "Evidence shown in the web report must be short, redacted, and appropriate for report display. Raw headers, cookies, API keys, "
    "bearer tokens, private keys, full private documents, large transcripts, and real customer data are not stored "
    "or displayed by the Phase 18 report foundation."
)


def build_severity_breakdown(findings: Iterable[Any]) -> SeverityBreakdown:
    counts = {severity: 0 for severity in SEVERITY_RANK}
    for finding in findings or []:
        severity = normalize_severity(str(_get(finding, "severity", "informational") or "informational"))
        counts[severity] += 1
    return SeverityBreakdown(
        critical=counts["critical"],
        high=counts["high"],
        medium=counts["medium"],
        low=counts["low"],
        informational=counts["informational"],
    )


def select_top_fixes(findings: Iterable[Any], limit: int = 3) -> List[TopFix]:
    """Select deduplicated top fixes by severity, confidence, and impact."""
    by_fix: dict[str, TopFix] = {}
    for finding in findings or []:
        status = _status(finding)
        if status in {"fixed", "false_positive"}:
            continue
        recommendation = _clean(_get(finding, "fix_recommendation", "")) or _clean(
            _get(finding, "fix_recommendation_summary", "")
        )
        if not recommendation:
            continue
        key = _dedupe_key(recommendation)
        candidate = TopFix(
            title=_clean(_get(finding, "title", "")),
            severity=_severity(finding),
            confidence=_confidence(finding),
            category=_category(finding),
            finding_ids=[_clean(_get(finding, "finding_id", ""))],
            recommendation=recommendation,
            business_impact_summary=_summary(_get(finding, "business_impact_summary", "") or _get(finding, "business_impact", "")),
        )
        if key not in by_fix:
            by_fix[key] = candidate
            continue
        existing = by_fix[key]
        existing.finding_ids.extend([item for item in candidate.finding_ids if item and item not in existing.finding_ids])
        if _sort_tuple(candidate) < _sort_tuple(existing):
            candidate.finding_ids = existing.finding_ids
            by_fix[key] = candidate

    return sorted(by_fix.values(), key=_sort_tuple)[:limit]


def shape_findings_table(findings: Iterable[Any]) -> List[dict[str, str]]:
    rows: List[dict[str, str]] = []
    for finding in findings or []:
        category = _category(finding)
        rows.append(
            {
                "finding_id": _clean(_get(finding, "finding_id", "")),
                "title": _clean(_get(finding, "title", "")),
                "category": category,
                "category_display_name": category_display_name(category),
                "severity": _severity(finding),
                "confidence": _confidence(finding),
                "status": _status(finding),
                "business_impact_summary": _summary(
                    _get(finding, "business_impact_summary", "") or _get(finding, "business_impact", "")
                ),
                "fix_recommendation_summary": _summary(
                    _get(finding, "fix_recommendation_summary", "") or _get(finding, "fix_recommendation", "")
                ),
            }
        )
    return rows


def report_finding_from_finding(finding: Any) -> ReportFinding:
    category = _category(finding)
    evidence_summary = redacted_report_evidence_summary(_get(finding, "evidence_summary", ""))
    evidence_items = format_report_evidence_items(_get(finding, "evidence_items", []), fallback=evidence_summary)
    business_impact = _clean(_get(finding, "business_impact", ""))
    fix_recommendation = _clean(_get(finding, "fix_recommendation", ""))
    manual_note = _clean(_get(finding, "manual_review_notes", ""))
    if bool(_get(finding, "manual_review_required", False)) and not manual_note:
        manual_note = "Manual review is required before treating this finding as final."
    limitations = []
    if _status(finding) == "needs_review":
        limitations.append("Finding status is needs_review, so impact and remediation priority require human confirmation.")
    if _confidence(finding) == "low":
        limitations.append("Low confidence evidence should not be treated as conclusive without manual review.")

    return ReportFinding(
        finding_id=_clean(_get(finding, "finding_id", "")),
        title=_clean(_get(finding, "title", "")),
        category=category,
        category_display_name=category_display_name(category),
        severity=_severity(finding),
        confidence=_confidence(finding),
        status=_status(finding),
        description=_clean(_get(finding, "description", "")),
        business_impact=business_impact,
        business_impact_summary=_summary(business_impact),
        evidence_summary=evidence_summary,
        evidence_items=evidence_items,
        reproduction_steps=[_clean(step) for step in _get(finding, "reproduction_steps", []) if _clean(step)],
        fix_recommendation=fix_recommendation,
        fix_recommendation_summary=_summary(fix_recommendation),
        manual_review_note=manual_note,
        limitations=limitations,
        source_test_ids=list(_get(finding, "source_test_ids", []) or []),
        metadata=dict(_get(finding, "metadata", {}) or {}),
    )


def format_tested_categories(categories: Iterable[Any]) -> List[TestedCategory]:
    formatted: List[TestedCategory] = []
    for item in categories or []:
        if isinstance(item, dict):
            category = normalize_category(str(item.get("category") or item.get("name") or ""))
            notes = _clean(item.get("notes", ""))
            status = _clean(item.get("status", "tested")) or "tested"
        else:
            category = normalize_category(str(item))
            notes = ""
            status = "tested"
        if category == "other_unknown":
            continue
        if category not in {entry.category for entry in formatted}:
            formatted.append(
                TestedCategory(
                    category=category,
                    display_name=category_display_name(category),
                    status=status,
                    notes=notes,
                )
            )
    return formatted


def build_limitations(extra_limitations: Iterable[str] | None = None) -> List[str]:
    limitations: List[str] = []
    for item in list(DEFAULT_LIMITATIONS) + list(extra_limitations or []):
        text = _clean(str(item))
        if text and text not in limitations:
            limitations.append(text)
    return limitations


def build_executive_summary(findings: Iterable[ReportFinding], verdict_label: str, score: int) -> str:
    finding_list = list(findings or [])
    if not finding_list:
        return (
            f"The report has a {score}/100 score and a {verdict_label} verdict for the documented scope. "
            "No findings were supplied to the report builder, but this does not mean untested categories are free of risk."
        )
    breakdown = build_severity_breakdown(finding_list)
    return (
        f"The report has a {score}/100 score and a {verdict_label} verdict for the documented scope. "
        f"It includes {breakdown.total} finding(s): {breakdown.critical} Critical, {breakdown.high} High, "
        f"{breakdown.medium} Medium, {breakdown.low} Low, and {breakdown.informational} Informational. "
        "Prioritize active Critical and High findings, then retest the original scenarios after remediation."
    )


def _sort_tuple(fix: TopFix) -> tuple[int, int, int, str]:
    return (
        -SEVERITY_RANK[normalize_severity(fix.severity)],
        -CONFIDENCE_RANK[normalize_confidence(fix.confidence)],
        -_business_impact_weight(fix.business_impact_summary),
        fix.title,
    )


def _business_impact_weight(text: str) -> int:
    value = text.lower()
    keywords = (
        "customer",
        "tenant",
        "credential",
        "token",
        "private",
        "unauthorized",
        "financial",
        "production",
        "outage",
        "sensitive",
        "regulated",
    )
    return sum(1 for keyword in keywords if keyword in value)


def _dedupe_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _summary(value: Any, max_chars: int = 180) -> str:
    text = _clean(str(value or ""))
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3].rstrip()}..."


def _severity(finding: Any) -> str:
    return normalize_severity(str(_get(finding, "severity", "informational") or "informational"))


def _confidence(finding: Any) -> str:
    return normalize_confidence(str(_get(finding, "confidence", "low") or "low"))


def _status(finding: Any) -> str:
    try:
        return normalize_status(str(_get(finding, "status", "needs_review") or "needs_review"))
    except ValueError:
        return "needs_review"


def _category(finding: Any) -> str:
    return normalize_category(str(_get(finding, "category", "other_unknown") or "other_unknown"))


def _clean(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _get(item: Any, name: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)
