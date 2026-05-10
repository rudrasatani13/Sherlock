from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .common import ModuleStatus


class ReportsModuleStatus(ModuleStatus):
    module: str = "reports"
    status: str = "web_report_foundation"
    purpose: str = "Phase 18 web report schema metadata and report access placeholder after findings are reviewed."
    future_phase: str = "Phase 19 PDF export after web report foundation"


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
        "PDF export",
        "downloadable report assets",
        "billing gates",
        "real report sharing tokens",
        "public report links with access control",
        "public scan execution",
        "real customer evidence storage",
    ])
