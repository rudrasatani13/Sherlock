"""Redacted evidence formatting for Phase 18 web reports."""
from __future__ import annotations

from typing import Any, Iterable, List

from packages.findings_system.evidence import (
    contains_unredacted_sensitive_marker,
    redact_evidence_text,
    summarize_evidence,
)

from .models import EvidenceSnippet


MAX_REPORT_EVIDENCE_CHARS = 240


def redacted_report_evidence_summary(value: str | None, max_chars: int = MAX_REPORT_EVIDENCE_CHARS) -> str:
    """Return short, redacted evidence text suitable for a web report."""
    return summarize_evidence(redact_evidence_text(value or ""), max_chars=max_chars)


def format_report_evidence_items(items: Iterable[Any], fallback: str = "") -> List[EvidenceSnippet]:
    """Convert Phase 17 evidence items or dicts into redacted report snippets."""
    snippets: List[EvidenceSnippet] = []
    for item in items or []:
        signal = _get(item, "signal", "evidence")
        summary = redacted_report_evidence_summary(_get(item, "summary", ""))
        redacted = redacted_report_evidence_summary(_get(item, "redacted_snippet", "") or summary)
        source_test_id = str(_get(item, "source_test_id", "") or "")
        if summary or redacted:
            snippets.append(
                EvidenceSnippet(
                    signal=str(signal or "evidence"),
                    summary=summary or redacted,
                    redacted_snippet=redacted or summary,
                    source_test_id=source_test_id,
                )
            )

    if not snippets and fallback:
        redacted_fallback = redacted_report_evidence_summary(fallback)
        if redacted_fallback:
            snippets.append(
                EvidenceSnippet(
                    signal="evidence_summary",
                    summary=redacted_fallback,
                    redacted_snippet=redacted_fallback,
                )
            )

    for snippet in snippets:
        if contains_unredacted_sensitive_marker(snippet.summary) or contains_unredacted_sensitive_marker(snippet.redacted_snippet):
            raise ValueError("report evidence contains an unredacted sensitive marker")
    return snippets


def _get(item: Any, name: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)
