"""PDF export section builder for Phase 18 report objects."""
from __future__ import annotations

from typing import Any

from packages.report_system.models import Report
from packages.report_system.sections import shape_findings_table

from .models import (
    DEFAULT_EVIDENCE_HANDLING_NOTE,
    PDF_EXPORT_SYSTEM_VERSION,
    PDF_EXPORT_TYPE_PRINT_HTML,
    CoverPage,
    PdfDetailedFinding,
    PdfFindingTableRow,
    PdfReportExport,
    safe_report_filename,
    stable_export_id,
    utc_now_iso,
)
from .safety import validate_pdf_export_safety, validate_pdf_evidence_text


def build_pdf_export_from_report(
    report: Report,
    *,
    export_type: str = PDF_EXPORT_TYPE_PRINT_HTML,
    export_status: str = "draft",
    generated_at: str | None = None,
) -> PdfReportExport:
    """Build a safe Phase 19 export object from a Phase 18 Report."""
    created_at = generated_at or utc_now_iso()
    filename = safe_report_filename(report.report_id, export_type)
    export = PdfReportExport(
        export_id=stable_export_id(report.report_id, export_type, created_at),
        report_id=report.report_id,
        export_status=export_status,
        export_type=export_type,
        title=f"{report.title} PDF Export",
        filename=filename,
        generated_at=created_at,
        cover_page=CoverPage(
            product_name="Sherlock",
            brand="PowerDetect",
            report_title=report.title,
            project_name=report.project_name,
            target_name=report.target_name,
            scan_type=report.scan_type,
            report_date=report.generated_at,
            report_id=report.report_id,
            demo_static_label="Phase 19 PDF export foundation - static/demo only",
        ),
        executive_summary=report.executive_summary,
        verdict=report.launch_readiness_verdict.to_dict(),
        score=report.security_score.to_dict(),
        severity_breakdown=report.severity_breakdown.to_dict(),
        top_fixes=[fix.to_dict() for fix in report.top_fixes],
        findings_table=_build_findings_table(report),
        detailed_findings=_build_detailed_findings(report),
        tested_categories=[item.to_dict() for item in report.tested_categories],
        not_tested=report.not_tested,
        limitations=report.limitations,
        evidence_handling_note=report.evidence_handling_note or DEFAULT_EVIDENCE_HANDLING_NOTE,
        source_report_id=report.report_id,
        metadata={
            "pdf_export_system_version": PDF_EXPORT_SYSTEM_VERSION,
            "phase": "phase_19_pdf_export_foundation",
            "current_behavior": "print-ready HTML/export contract foundation only",
            "source_report_system_version": report.metadata.get("report_system_version", ""),
            "disabled_capabilities": [
                "production PDF export for real customer reports",
                "public PDF download links",
                "public report sharing",
                "billing or Stripe",
                "real paid-plan enforcement",
                "active report database persistence",
                "production storage integration",
                "real customer evidence storage",
                "Phase 20 retest flow",
            ],
        },
    )
    validate_pdf_export_safety(export)
    return export


def _build_findings_table(report: Report) -> list[PdfFindingTableRow]:
    rows: list[PdfFindingTableRow] = []
    for row in shape_findings_table(report.findings):
        rows.append(
            PdfFindingTableRow(
                finding_id=row["finding_id"],
                title=row["title"],
                category=row["category_display_name"],
                severity=row["severity"],
                confidence=row["confidence"],
                status=row["status"],
                business_impact_summary=row["business_impact_summary"],
                fix_recommendation_summary=row["fix_recommendation_summary"],
            )
        )
    return rows


def _build_detailed_findings(report: Report) -> list[PdfDetailedFinding]:
    detailed: list[PdfDetailedFinding] = []
    for finding in report.findings:
        snippets = []
        for item in finding.evidence_items:
            snippet = item.redacted_snippet or item.summary
            validate_pdf_evidence_text(snippet)
            if snippet and snippet not in snippets:
                snippets.append(snippet)
        if not snippets and finding.evidence_summary:
            validate_pdf_evidence_text(finding.evidence_summary)
            snippets.append(finding.evidence_summary)
        detailed.append(
            PdfDetailedFinding(
                finding_id=finding.finding_id,
                title=finding.title,
                category=finding.category_display_name,
                severity=finding.severity,
                confidence=finding.confidence,
                status=finding.status,
                description=finding.description,
                business_impact=finding.business_impact,
                evidence_snippets=snippets,
                reproduction_steps=finding.reproduction_steps,
                fix_recommendation=finding.fix_recommendation,
                limitations=finding.limitations,
                retest_status=report.retest_status,
            )
        )
    return detailed
