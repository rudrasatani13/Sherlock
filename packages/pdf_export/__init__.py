"""Phase 19 PDF export foundation for PowerDetect Sherlock."""
from __future__ import annotations

from .models import (
    PDF_EXPORT_STATUSES,
    PDF_EXPORT_TYPES,
    PDF_EXPORT_STATUS_ARCHIVED,
    PDF_EXPORT_STATUS_BLOCKED_SENSITIVE_EVIDENCE,
    PDF_EXPORT_STATUS_DRAFT,
    PDF_EXPORT_STATUS_FAILED,
    PDF_EXPORT_STATUS_READY,
    PDF_EXPORT_TYPE_PDF,
    PDF_EXPORT_TYPE_PREVIEW,
    PDF_EXPORT_TYPE_PRINT_HTML,
    CoverPage,
    PdfDetailedFinding,
    PdfFindingTableRow,
    PdfReportExport,
    normalize_export_status,
    normalize_export_type,
    safe_report_filename,
)
from .renderer import render_print_html, write_print_html
from .safety import resolve_export_path, validate_pdf_export_safety, validate_pdf_evidence_text
from .template import build_pdf_export_from_report

__all__ = [
    "PDF_EXPORT_STATUSES",
    "PDF_EXPORT_TYPES",
    "PDF_EXPORT_STATUS_ARCHIVED",
    "PDF_EXPORT_STATUS_BLOCKED_SENSITIVE_EVIDENCE",
    "PDF_EXPORT_STATUS_DRAFT",
    "PDF_EXPORT_STATUS_FAILED",
    "PDF_EXPORT_STATUS_READY",
    "PDF_EXPORT_TYPE_PDF",
    "PDF_EXPORT_TYPE_PREVIEW",
    "PDF_EXPORT_TYPE_PRINT_HTML",
    "CoverPage",
    "PdfDetailedFinding",
    "PdfFindingTableRow",
    "PdfReportExport",
    "build_pdf_export_from_report",
    "normalize_export_status",
    "normalize_export_type",
    "render_print_html",
    "resolve_export_path",
    "safe_report_filename",
    "validate_pdf_evidence_text",
    "validate_pdf_export_safety",
    "write_print_html",
]
