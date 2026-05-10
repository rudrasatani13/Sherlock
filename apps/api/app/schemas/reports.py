from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .common import ModuleStatus


class ReportsModuleStatus(ModuleStatus):
    module: str = "reports"
    status: str = "pdf_export_foundation"
    purpose: str = "Phase 19 report and PDF export schema metadata. Report access and customer PDF delivery remain placeholders."
    future_phase: str = "Future production report access, secure storage, paid gates, and delivery after auth and persistence exist"


class ReportsContract(BaseModel):
    """Static Phase 18 web report contract metadata.

    This is not a persistence schema and does not return customer reports.
    """

    current_behavior: str = "Static contract metadata only. No route reads or writes report records."
    package: str = "packages.report_system"
    report_statuses: List[str] = Field(default_factory=list)
    report_types: List[str] = Field(default_factory=list)
    launch_readiness_verdicts: List[str] = Field(default_factory=list)
    required_fields: List[str] = Field(default_factory=lambda: [
        "report_id",
        "report_type",
        "title",
        "project_name",
        "target_name",
        "scan_type",
        "report_status",
        "generated_at",
        "launch_readiness_verdict",
        "security_score",
        "executive_summary",
        "severity_breakdown",
        "top_fixes",
        "findings",
        "tested_categories",
        "not_tested",
        "limitations",
        "evidence_handling_note",
        "retest_status",
        "methodology_version",
        "findings_system_version",
        "source_scan_id",
        "metadata",
    ])
    score_rules: List[str] = Field(default_factory=lambda: [
        "score is bounded from 0 to 100",
        "no findings does not automatically score 100",
        "critical findings heavily reduce and cap score",
        "high findings materially reduce and cap score",
        "needs_review findings cap score confidence",
        "false positives do not reduce score",
    ])
    evidence_rules: List[str] = Field(default_factory=lambda: [
        "evidence must be redacted and short",
        "raw headers, cookies, API keys, bearer tokens, private keys, private documents, large transcripts, and real customer data are not returned",
        "Phase 18 uses Phase 17 evidence redaction helpers",
    ])
    disabled_capabilities: List[str] = Field(default_factory=lambda: [
        "active report persistence",
        "report database writes",
        "real customer report retrieval",
        "production PDF export for real customer reports",
        "public PDF download links",
        "downloadable customer report assets",
        "billing gates",
        "real report sharing tokens",
        "public report links with access control",
        "public scan execution",
        "real customer evidence storage",
    ])


class PdfExportContract(BaseModel):
    """Static Phase 19 PDF export contract metadata.

    This is not a production export endpoint and does not write customer files.
    """

    current_behavior: str = "Static contract metadata plus internal package support for local/demo print-ready HTML exports only."
    package: str = "packages.pdf_export"
    export_statuses: List[str] = Field(default_factory=list)
    export_types: List[str] = Field(default_factory=list)
    required_fields: List[str] = Field(default_factory=lambda: [
        "export_id",
        "report_id",
        "export_status",
        "export_type",
        "title",
        "filename",
        "generated_at",
        "cover_page",
        "executive_summary",
        "verdict",
        "score",
        "severity_breakdown",
        "top_fixes",
        "findings_table",
        "detailed_findings",
        "tested_categories",
        "not_tested",
        "limitations",
        "evidence_handling_note",
        "footer_disclaimer",
        "source_report_id",
        "metadata",
    ])
    output_artifact_rules: List[str] = Field(default_factory=lambda: [
        "local generated HTML/PDF artifacts must stay in ignored directories",
        "allowed local directories are pdf-output, pdf-exports, and report-exports",
        "filenames use the powerdetect-sherlock-report prefix",
        "path traversal and unsafe path characters are rejected",
    ])
    evidence_safety_rules: List[str] = Field(default_factory=lambda: [
        "evidence must be redacted, short, and report-safe",
        "raw Authorization headers are blocked",
        "raw cookies are blocked",
        "API keys, bearer tokens, private keys, full private documents, large transcripts, and real customer data are blocked",
        "exports require limitations and careful non-overclaiming verdict language",
    ])
    disabled_capabilities: List[str] = Field(default_factory=lambda: [
        "production PDF export for real customer reports",
        "public PDF download links",
        "public report sharing",
        "billing or Stripe",
        "live paid-plan gates",
        "active report database persistence",
        "report database writes",
        "production storage integration",
        "email delivery",
        "admin panel",
        "real customer evidence storage",
        "public scan execution",
        "Phase 20 retest flow",
    ])
