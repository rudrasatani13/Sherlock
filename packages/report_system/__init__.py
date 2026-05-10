"""Phase 18 web report foundation for PowerDetect Sherlock."""
from __future__ import annotations

from .builder import build_report
from .evidence import format_report_evidence_items, redacted_report_evidence_summary
from .models import (
    LAUNCH_READINESS_VERDICTS,
    REPORT_STATUSES,
    REPORT_TYPES,
    LaunchReadinessVerdict,
    Report,
    ReportFinding,
    SecurityScore,
    SeverityBreakdown,
    TestedCategory,
    TopFix,
)
from .scoring import calculate_security_score
from .sections import (
    build_limitations,
    build_severity_breakdown,
    format_tested_categories,
    select_top_fixes,
    shape_findings_table,
)
from .verdicts import select_launch_readiness_verdict

__all__ = [
    "LAUNCH_READINESS_VERDICTS",
    "REPORT_STATUSES",
    "REPORT_TYPES",
    "LaunchReadinessVerdict",
    "Report",
    "ReportFinding",
    "SecurityScore",
    "SeverityBreakdown",
    "TestedCategory",
    "TopFix",
    "build_limitations",
    "build_report",
    "build_severity_breakdown",
    "calculate_security_score",
    "format_report_evidence_items",
    "format_tested_categories",
    "redacted_report_evidence_summary",
    "select_launch_readiness_verdict",
    "select_top_fixes",
    "shape_findings_table",
]
