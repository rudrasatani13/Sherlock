"""Redacted evidence helpers for Phase 17 findings."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

try:
    from packages.evaluator_system.evidence import redact_text as evaluator_redact_text
except Exception:  # pragma: no cover - fallback only if package layout changes.
    evaluator_redact_text = None


MAX_EVIDENCE_CHARS = 280

HEADER_LINE_RE = re.compile(
    r"(?im)^(authorization|cookie|set-cookie|x-api-key|api-key|proxy-authorization|x-auth-token)\s*:\s*.+$"
)
RAW_COOKIE_RE = re.compile(r"(?i)\b(cookie|set-cookie)\s*[:=]\s*(?!\[REDACTED_COOKIE\])[^;\n]+(?:;[^\n]*)?")
PRIVATE_DOC_RE = re.compile(r"(?is)<\s*(private_document|document|raw_transcript)\b.*?</\s*\1\s*>")
MULTISPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class EvidenceItem:
    """A short, redacted evidence reference for report use."""

    signal: str
    summary: str
    redacted_snippet: str
    source_test_id: str = ""
    strong_evidence: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal": self.signal,
            "summary": self.summary,
            "redacted_snippet": self.redacted_snippet,
            "source_test_id": self.source_test_id,
            "strong_evidence": self.strong_evidence,
        }


def redact_evidence_text(text: str | None) -> str:
    """Redact secrets, headers, cookies, canaries, and long raw snippets."""
    value = text or ""
    value = HEADER_LINE_RE.sub(r"\1: [REDACTED_HEADER]", value)
    value = RAW_COOKIE_RE.sub(r"\1=[REDACTED_COOKIE]", value)
    value = PRIVATE_DOC_RE.sub("[REDACTED_PRIVATE_DOCUMENT]", value)
    if evaluator_redact_text is not None:
        value = evaluator_redact_text(value)
    return value


def summarize_evidence(text: str | None, max_chars: int = MAX_EVIDENCE_CHARS) -> str:
    """Return a compact redacted evidence summary."""
    redacted = redact_evidence_text(text)
    compact = MULTISPACE_RE.sub(" ", redacted).strip()
    if len(compact) <= max_chars:
        return compact
    return f"{compact[: max_chars - 3].rstrip()}..."


def make_evidence_item(
    *,
    signal: str,
    snippet: str | None,
    source_test_id: str = "",
    strong_evidence: bool = False,
) -> EvidenceItem:
    safe_signal = (signal or "evaluator_signal").strip() or "evaluator_signal"
    summary = summarize_evidence(snippet)
    return EvidenceItem(
        signal=safe_signal,
        summary=summary,
        redacted_snippet=summary,
        source_test_id=source_test_id or "",
        strong_evidence=strong_evidence,
    )


def evidence_summary(items: Iterable[EvidenceItem], fallback: str = "") -> str:
    """Combine unique evidence item summaries into a short paragraph."""
    summaries: List[str] = []
    for item in items:
        if item.summary and item.summary not in summaries:
            summaries.append(item.summary)
    if not summaries:
        return summarize_evidence(fallback)
    return summarize_evidence(" | ".join(summaries))


def contains_unredacted_sensitive_marker(text: str | None) -> bool:
    """Best-effort check used by tests to keep report evidence safe."""
    value = text or ""
    value = re.sub(
        r"(?im)^(authorization|cookie|set-cookie|x-api-key|api-key|proxy-authorization|x-auth-token)\s*:\s*\[REDACTED_[A-Z_]+\]$",
        "",
        value,
    )
    if HEADER_LINE_RE.search(value) or RAW_COOKIE_RE.search(value):
        return True
    secret_patterns = (
        r"-----BEGIN [A-Z0-9 ]{0,48}PRIVATE KEY-----",
        r"\bBearer\s+[A-Za-z0-9._\-]{12,}\b",
        r"\b(password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|token)\b\s*[:=]\s*(?!\[REDACTED)[^\s,'\";]{4,}",
        r"\b(?:sk|pk|rk|ghp|github_pat|xoxb|xoxp|AIza|AKIA)[A-Za-z0-9._\-]{12,}\b",
    )
    return any(re.search(pattern, value, re.IGNORECASE) for pattern in secret_patterns)
