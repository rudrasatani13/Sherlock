"""Safety checks for Phase 19 PDF export artifacts."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from packages.findings_system.evidence import contains_unredacted_sensitive_marker

from .models import PdfDetailedFinding, PdfReportExport


ALLOWED_OUTPUT_DIRECTORIES: tuple[str, ...] = ("pdf-output", "pdf-exports", "report-exports")
MAX_PDF_EVIDENCE_CHARS = 220

_RAW_AUTH_RE = re.compile(r"(?im)^\s*authorization\s*:\s*(?!\[REDACTED_HEADER\]).+$")
_RAW_COOKIE_RE = re.compile(r"(?im)^\s*(cookie|set-cookie)\s*:\s*(?!\[REDACTED_COOKIE\]).+$")
_PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z0-9 ]{0,48}PRIVATE KEY-----", re.IGNORECASE)
_PRIVATE_DOC_RE = re.compile(r"(?is)<\s*(private_document|document|raw_transcript)\b")
_OVERCLAIMING_RE = re.compile(
    r"\b(guarantee(?:d|s)?|certified|fully secure|no risk|all vulnerabilities|100%\s*(?:secure|protected))\b",
    re.IGNORECASE,
)
_UNSAFE_PATH_CHARS_RE = re.compile(r"[\\/:\x00]")


def validate_pdf_export_safety(export: PdfReportExport) -> None:
    """Raise ValueError if an export object is unsafe for a downloadable report."""
    if _UNSAFE_PATH_CHARS_RE.search(export.title):
        raise ValueError("PDF export title contains unsafe path characters")
    validate_safe_filename(export.filename)
    if not export.limitations:
        raise ValueError("PDF export requires limitations")
    verdict_text = " ".join(str(value) for value in export.verdict.values())
    if _OVERCLAIMING_RE.search(verdict_text):
        raise ValueError("PDF export verdict uses overclaiming language")
    _validate_text_collection(
        [
            export.executive_summary,
            export.evidence_handling_note,
            export.footer_disclaimer,
            *export.not_tested,
            *export.limitations,
        ]
    )
    for finding in export.detailed_findings:
        validate_pdf_finding_safety(finding)


def validate_pdf_finding_safety(finding: PdfDetailedFinding) -> None:
    _validate_text_collection(
        [
            finding.title,
            finding.description,
            finding.business_impact,
            finding.fix_recommendation,
            *finding.reproduction_steps,
            *finding.limitations,
        ]
    )
    for snippet in finding.evidence_snippets:
        validate_pdf_evidence_text(snippet)


def validate_pdf_evidence_text(text: str | None) -> None:
    value = text or ""
    if len(value) > MAX_PDF_EVIDENCE_CHARS:
        raise ValueError("PDF evidence snippet is too long")
    if (
        contains_unredacted_sensitive_marker(value)
        or _RAW_AUTH_RE.search(value)
        or _RAW_COOKIE_RE.search(value)
        or _PRIVATE_KEY_RE.search(value)
        or _PRIVATE_DOC_RE.search(value)
    ):
        raise ValueError("PDF evidence contains unredacted sensitive material")


def validate_safe_filename(filename: str) -> None:
    value = filename or ""
    if not value:
        raise ValueError("PDF export filename is required")
    if "/" in value or "\\" in value or "\x00" in value or value in {".", ".."}:
        raise ValueError("PDF export filename must not contain path separators or traversal")
    if not value.startswith("powerdetect-sherlock-report-"):
        raise ValueError("PDF export filename must use the PowerDetect Sherlock report prefix")
    if not (value.endswith(".pdf") or value.endswith(".html")):
        raise ValueError("PDF export filename must end in .pdf or .html")


def resolve_export_path(output_dir: str | Path, filename: str, *, base_dir: str | Path = ".") -> Path:
    """Resolve an export path under an allowed ignored output directory."""
    validate_safe_filename(filename)
    output_path = Path(output_dir)
    if output_path.is_absolute():
        raise ValueError("PDF export output directory must be repository-relative")
    if any(part in {"", ".", ".."} for part in output_path.parts):
        raise ValueError("PDF export output directory must not use traversal")
    if not output_path.parts or output_path.parts[0] not in ALLOWED_OUTPUT_DIRECTORIES:
        raise ValueError("PDF export output directory must be pdf-output, pdf-exports, or report-exports")

    base_path = Path(base_dir).resolve()
    resolved_output_dir = (base_path / output_path).resolve()
    resolved_target = (resolved_output_dir / filename).resolve()
    try:
        resolved_target.relative_to(resolved_output_dir)
    except ValueError as exc:
        raise ValueError("PDF export target escapes the output directory") from exc
    return resolved_target


def _validate_text_collection(values: Iterable[str]) -> None:
    for value in values:
        text = value or ""
        if _RAW_AUTH_RE.search(text) or _RAW_COOKIE_RE.search(text) or _PRIVATE_KEY_RE.search(text) or _PRIVATE_DOC_RE.search(text):
            raise ValueError("PDF export text contains raw sensitive material")
