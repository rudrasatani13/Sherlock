"""PDF export data contracts for the Phase 19 foundation."""
from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Dict, List

from packages.report_system.models import utc_now_iso


PDF_EXPORT_STATUS_DRAFT = "draft"
PDF_EXPORT_STATUS_READY = "ready"
PDF_EXPORT_STATUS_BLOCKED_SENSITIVE_EVIDENCE = "blocked_sensitive_evidence"
PDF_EXPORT_STATUS_FAILED = "failed"
PDF_EXPORT_STATUS_ARCHIVED = "archived"

PDF_EXPORT_STATUSES: tuple[str, ...] = (
    PDF_EXPORT_STATUS_DRAFT,
    PDF_EXPORT_STATUS_READY,
    PDF_EXPORT_STATUS_BLOCKED_SENSITIVE_EVIDENCE,
    PDF_EXPORT_STATUS_FAILED,
    PDF_EXPORT_STATUS_ARCHIVED,
)

PDF_EXPORT_TYPE_PDF = "pdf"
PDF_EXPORT_TYPE_PRINT_HTML = "print_html"
PDF_EXPORT_TYPE_PREVIEW = "preview"

PDF_EXPORT_TYPES: tuple[str, ...] = (
    PDF_EXPORT_TYPE_PDF,
    PDF_EXPORT_TYPE_PRINT_HTML,
    PDF_EXPORT_TYPE_PREVIEW,
)

PDF_EXPORT_SYSTEM_VERSION = "phase_19_pdf_export_foundation_v0.1"
DEFAULT_FOOTER_DISCLAIMER = (
    "PowerDetect Sherlock reports describe observed behavior in the documented tested scope. "
    "They are not a guarantee of security, a certification, or proof that all vulnerabilities were found."
)
DEFAULT_EVIDENCE_HANDLING_NOTE = (
    "PDF export evidence is short, redacted, and report-safe. Raw headers, cookies, API keys, "
    "bearer tokens, private keys, full private documents, large transcripts, and real customer data "
    "must not be included in downloadable reports."
)

_SAFE_ID_RE = re.compile(r"[^a-zA-Z0-9-]+")


def normalize_export_status(value: str | None) -> str:
    normalized = (value or PDF_EXPORT_STATUS_DRAFT).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in PDF_EXPORT_STATUSES:
        raise ValueError(f"unsupported PDF export status: {value}")
    return normalized


def normalize_export_type(value: str | None) -> str:
    normalized = (value or PDF_EXPORT_TYPE_PRINT_HTML).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in PDF_EXPORT_TYPES:
        raise ValueError(f"unsupported PDF export type: {value}")
    return normalized


def stable_export_id(*parts: str) -> str:
    digest = hashlib.sha256("|".join(str(part or "") for part in parts).encode("utf-8")).hexdigest()[:12]
    return f"shk_pdf_export_{digest}"


def safe_report_filename(report_id: str, export_type: str = PDF_EXPORT_TYPE_PRINT_HTML) -> str:
    """Return a traversal-safe PowerDetect Sherlock report filename."""
    normalized_type = normalize_export_type(export_type)
    extension = "pdf" if normalized_type == PDF_EXPORT_TYPE_PDF else "html"
    cleaned_id = _SAFE_ID_RE.sub("-", str(report_id or "demo").strip()).strip(".-").lower()
    cleaned_id = cleaned_id or "demo"
    return f"powerdetect-sherlock-report-{cleaned_id}.{extension}"


@dataclass
class CoverPage:
    product_name: str
    brand: str
    report_title: str
    project_name: str
    target_name: str
    scan_type: str
    report_date: str
    report_id: str
    demo_static_label: str = "Static demo export foundation"
    disclaimer: str = DEFAULT_FOOTER_DISCLAIMER

    def __post_init__(self) -> None:
        self.product_name = _clean_text(self.product_name or "Sherlock")
        self.brand = _clean_text(self.brand or "PowerDetect")
        self.report_title = _clean_text(self.report_title)
        self.project_name = _clean_text(self.project_name)
        self.target_name = _clean_text(self.target_name)
        self.scan_type = _clean_text(self.scan_type)
        self.report_date = _clean_text(self.report_date)
        self.report_id = _clean_text(self.report_id)
        self.demo_static_label = _clean_text(self.demo_static_label)
        self.disclaimer = _clean_text(self.disclaimer or DEFAULT_FOOTER_DISCLAIMER)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class PdfFindingTableRow:
    finding_id: str
    title: str
    category: str
    severity: str
    confidence: str
    status: str
    business_impact_summary: str
    fix_recommendation_summary: str

    def __post_init__(self) -> None:
        self.finding_id = _clean_text(self.finding_id)
        self.title = _clean_text(self.title)
        self.category = _clean_text(self.category)
        self.severity = _clean_text(self.severity)
        self.confidence = _clean_text(self.confidence)
        self.status = _clean_text(self.status)
        self.business_impact_summary = _clean_text(self.business_impact_summary)
        self.fix_recommendation_summary = _clean_text(self.fix_recommendation_summary)

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class PdfDetailedFinding:
    finding_id: str
    title: str
    category: str
    severity: str
    confidence: str
    status: str
    description: str
    business_impact: str
    evidence_snippets: List[str] = field(default_factory=list)
    reproduction_steps: List[str] = field(default_factory=list)
    fix_recommendation: str = ""
    limitations: List[str] = field(default_factory=list)
    retest_status: str = "not_retested"

    def __post_init__(self) -> None:
        self.finding_id = _clean_text(self.finding_id)
        self.title = _clean_text(self.title)
        self.category = _clean_text(self.category)
        self.severity = _clean_text(self.severity)
        self.confidence = _clean_text(self.confidence)
        self.status = _clean_text(self.status)
        self.description = _clean_text(self.description)
        self.business_impact = _clean_text(self.business_impact)
        self.evidence_snippets = _clean_list(self.evidence_snippets)
        self.reproduction_steps = _clean_list(self.reproduction_steps)
        self.fix_recommendation = _clean_text(self.fix_recommendation)
        self.limitations = _clean_list(self.limitations)
        self.retest_status = _clean_text(self.retest_status or "not_retested")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PdfReportExport:
    export_id: str
    report_id: str
    export_status: str
    export_type: str
    title: str
    filename: str
    generated_at: str
    cover_page: CoverPage
    executive_summary: str
    verdict: Dict[str, str]
    score: Dict[str, Any]
    severity_breakdown: Dict[str, int]
    top_fixes: List[Dict[str, Any]]
    findings_table: List[PdfFindingTableRow]
    detailed_findings: List[PdfDetailedFinding]
    tested_categories: List[Dict[str, str]]
    not_tested: List[str]
    limitations: List[str]
    evidence_handling_note: str = DEFAULT_EVIDENCE_HANDLING_NOTE
    footer_disclaimer: str = DEFAULT_FOOTER_DISCLAIMER
    source_report_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.report_id = _clean_text(self.report_id)
        self.export_type = normalize_export_type(self.export_type)
        self.export_status = normalize_export_status(self.export_status)
        self.export_id = _clean_text(self.export_id) or stable_export_id(
            self.report_id,
            self.export_type,
            self.generated_at,
        )
        self.title = _clean_text(self.title)
        self.filename = _clean_text(self.filename) or safe_report_filename(self.report_id, self.export_type)
        self.generated_at = _clean_text(self.generated_at) or utc_now_iso()
        self.executive_summary = _clean_text(self.executive_summary)
        self.not_tested = _clean_list(self.not_tested)
        self.limitations = _clean_list(self.limitations)
        self.evidence_handling_note = _clean_text(self.evidence_handling_note or DEFAULT_EVIDENCE_HANDLING_NOTE)
        self.footer_disclaimer = _clean_text(self.footer_disclaimer or DEFAULT_FOOTER_DISCLAIMER)
        self.source_report_id = _clean_text(self.source_report_id or self.report_id)
        if not self.limitations:
            raise ValueError("PDF exports must include limitations")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "export_id": self.export_id,
            "report_id": self.report_id,
            "export_status": self.export_status,
            "export_type": self.export_type,
            "title": self.title,
            "filename": self.filename,
            "generated_at": self.generated_at,
            "cover_page": self.cover_page.to_dict(),
            "executive_summary": self.executive_summary,
            "verdict": _plain(self.verdict),
            "score": _plain(self.score),
            "severity_breakdown": _plain(self.severity_breakdown),
            "top_fixes": _plain(self.top_fixes),
            "findings_table": [row.to_dict() for row in self.findings_table],
            "detailed_findings": [finding.to_dict() for finding in self.detailed_findings],
            "tested_categories": _plain(self.tested_categories),
            "not_tested": list(self.not_tested),
            "limitations": list(self.limitations),
            "evidence_handling_note": self.evidence_handling_note,
            "footer_disclaimer": self.footer_disclaimer,
            "source_report_id": self.source_report_id,
            "metadata": _plain(self.metadata),
        }


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
