"""Report builder for Phase 18 web report foundation."""
from __future__ import annotations

from typing import Any, Iterable

from .models import (
    REPORT_SYSTEM_VERSION,
    Report,
    stable_report_id,
    utc_now_iso,
)
from .scoring import calculate_security_score
from .sections import (
    EVIDENCE_HANDLING_NOTE,
    build_executive_summary,
    build_limitations,
    build_severity_breakdown,
    format_tested_categories,
    report_finding_from_finding,
    select_top_fixes,
)
from .verdicts import select_launch_readiness_verdict


def build_report(
    *,
    metadata: dict[str, Any] | None = None,
    findings: Iterable[Any] | None = None,
    tested_categories: Iterable[Any] | None = None,
    not_tested: Iterable[str] | None = None,
    limitations: Iterable[str] | None = None,
) -> Report:
    """Build a structured Report object from reviewed/static findings.

    Phase 18 does not read scan-result files, write report artifacts, persist
    reports, create share links, or generate PDFs. Callers pass sanitized findings
    and metadata explicitly.
    """
    meta = dict(metadata or {})
    source_findings = list(findings or [])
    report_findings = [report_finding_from_finding(item) for item in source_findings]
    tested = format_tested_categories(tested_categories or [])
    not_tested_list = _clean_list(list(not_tested or meta.get("not_tested", []) or []))
    report_limitations = build_limitations(limitations or meta.get("limitations", []))
    security_score = calculate_security_score(report_findings)
    verdict = select_launch_readiness_verdict(
        report_findings,
        security_score,
        tested_categories=tested,
        not_tested=not_tested_list,
    )
    generated_at = _clean(meta.get("generated_at", "")) or utc_now_iso()
    source_scan_id = _clean(meta.get("source_scan_id", "")) or _first_source_scan_id(source_findings)
    title = _clean(meta.get("title", "")) or "AI Launch Security Web Report"
    project_name = _clean(meta.get("project_name", "")) or "Demo project"
    target_name = _clean(meta.get("target_name", "")) or "Demo target"
    report_id = _clean(meta.get("report_id", "")) or stable_report_id(title, project_name, target_name, generated_at)

    executive_summary = _clean(meta.get("executive_summary", "")) or build_executive_summary(
        report_findings,
        verdict.label,
        security_score.score,
    )

    return Report(
        report_id=report_id,
        report_type=_clean(meta.get("report_type", "")) or "sample",
        title=title,
        project_name=project_name,
        target_name=target_name,
        scan_type=_clean(meta.get("scan_type", "")) or "static_demo",
        report_status=_clean(meta.get("report_status", "")) or "draft",
        generated_at=generated_at,
        launch_readiness_verdict=verdict,
        security_score=security_score,
        executive_summary=executive_summary,
        severity_breakdown=build_severity_breakdown(report_findings),
        top_fixes=select_top_fixes(report_findings),
        findings=report_findings,
        tested_categories=tested,
        not_tested=not_tested_list,
        limitations=report_limitations,
        evidence_handling_note=_clean(meta.get("evidence_handling_note", "")) or EVIDENCE_HANDLING_NOTE,
        retest_status=_clean(meta.get("retest_status", "")) or "not_retested",
        source_scan_id=source_scan_id,
        metadata={
            "report_system_version": REPORT_SYSTEM_VERSION,
            "phase": "phase_18_web_report_foundation",
            "current_behavior": "structured report object built from explicit sanitized/static findings only",
            "disabled_capabilities": [
                "PDF export",
                "billing gates",
                "active database persistence",
                "real report sharing links",
                "real customer evidence storage",
                "public scan execution",
            ],
            **dict(meta.get("metadata", {}) or {}),
        },
    )


def _first_source_scan_id(findings: Iterable[Any]) -> str:
    for finding in findings:
        value = _clean(_get(finding, "source_scan_id", ""))
        if value:
            return value
        metadata = _get(finding, "metadata", {}) or {}
        value = _clean(metadata.get("source_scan_id", "")) if isinstance(metadata, dict) else ""
        if value:
            return value
    return ""


def _clean(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _clean_list(values: list[Any]) -> list[str]:
    output: list[str] = []
    for value in values:
        text = _clean(value)
        if text and text not in output:
            output.append(text)
    return output


def _get(item: Any, name: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)
