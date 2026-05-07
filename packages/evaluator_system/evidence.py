from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Tuple

from .models import EvidenceSnippet

SNIPPET_WINDOW = 96
MAX_SNIPPET_LENGTH = 240

PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN [A-Z0-9 ]{0,48}PRIVATE KEY-----.*?-----END [A-Z0-9 ]{0,48}PRIVATE KEY-----",
    re.IGNORECASE | re.DOTALL,
)
BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{12,}\b", re.IGNORECASE)
ASSIGNMENT_SECRET_RE = re.compile(
    r"\b(password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|token)\b\s*[:=]\s*(['\"]?)[^\s,'\";]{4,}\2",
    re.IGNORECASE,
)
KEY_PREFIX_RE = re.compile(
    r"\b(?:sk|pk|rk|ghp|github_pat|xoxb|xoxp|AIza|AKIA)[A-Za-z0-9._\-]{12,}\b"
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.IGNORECASE)
LONG_TOKEN_RE = re.compile(r"\b[A-Za-z0-9_\-]{32,}\b")
CANARY_RE = re.compile(
    r"\b(?:(?:FAKE|DEMO|TEST|SHK|SHERLOCK)[-_A-Z0-9]*CANARY[-_A-Z0-9]*|CANARY[-_](?:FAKE|DEMO|TEST|SHK|SHERLOCK)[-_A-Z0-9]*)\b",
    re.IGNORECASE,
)


def make_evidence(text: str, start: int, end: int, signal: str) -> EvidenceSnippet:
    safe_text = text or ""
    safe_start = max(0, min(start, len(safe_text)))
    safe_end = max(safe_start, min(end, len(safe_text)))
    snippet_start = max(0, safe_start - SNIPPET_WINDOW)
    snippet_end = min(len(safe_text), safe_end + SNIPPET_WINDOW)
    if snippet_end - snippet_start > MAX_SNIPPET_LENGTH:
        snippet_end = min(len(safe_text), snippet_start + MAX_SNIPPET_LENGTH)
    snippet = safe_text[snippet_start:snippet_end]
    if snippet_end < len(safe_text):
        snippet = f"{snippet}..."
    return EvidenceSnippet(
        signal=signal,
        snippet=snippet,
        redacted_snippet=redact_text(snippet),
        start=safe_start,
        end=safe_end,
    )


def regex_evidence(text: str, pattern: re.Pattern[str], signal: str, limit: int = 5) -> List[EvidenceSnippet]:
    evidence: List[EvidenceSnippet] = []
    for match in pattern.finditer(text or ""):
        evidence.append(make_evidence(text, match.start(), match.end(), signal))
        if len(evidence) >= limit:
            break
    return evidence


def literal_evidence(text: str, literal: str, signal: str, limit: int = 5) -> List[EvidenceSnippet]:
    if not literal:
        return []
    haystack = text or ""
    haystack_lower = haystack.lower()
    needle_lower = literal.lower()
    evidence: List[EvidenceSnippet] = []
    cursor = 0
    while len(evidence) < limit:
        position = haystack_lower.find(needle_lower, cursor)
        if position < 0:
            break
        evidence.append(make_evidence(haystack, position, position + len(literal), signal))
        cursor = position + max(1, len(literal))
    return evidence


def redact_text(text: str) -> str:
    redacted = text or ""
    redacted = PRIVATE_KEY_RE.sub("[REDACTED_PRIVATE_KEY]", redacted)
    redacted = BEARER_RE.sub("Bearer [REDACTED_TOKEN]", redacted)
    redacted = ASSIGNMENT_SECRET_RE.sub(lambda match: f"{match.group(1)}=[REDACTED_SECRET]", redacted)
    redacted = KEY_PREFIX_RE.sub("[REDACTED_KEY]", redacted)
    redacted = EMAIL_RE.sub("[REDACTED_EMAIL]", redacted)
    redacted = CANARY_RE.sub("[REDACTED_CANARY]", redacted)
    redacted = LONG_TOKEN_RE.sub("[REDACTED_TOKEN]", redacted)
    return redacted


def collect_canary_tokens(metadata: Dict[str, Any]) -> List[str]:
    tokens: List[str] = []

    def add_token(value: str) -> None:
        normalized = value.strip().strip(".,;:()[]{}<>\"'")
        if len(normalized) >= 8 and normalized.lower() not in {item.lower() for item in tokens}:
            tokens.append(normalized)

    def visit(value: Any, key_path: Tuple[str, ...]) -> None:
        joined_key = ".".join(key_path).lower()
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                visit(child_value, key_path + (str(child_key),))
            return
        if isinstance(value, list):
            for index, child_value in enumerate(value):
                visit(child_value, key_path + (str(index),))
            return
        if not isinstance(value, str):
            return
        if "canary" in joined_key and CANARY_RE.fullmatch(value.strip()):
            add_token(value)
        for match in CANARY_RE.finditer(value):
            add_token(match.group(0))

    visit(metadata or {}, tuple())
    return tokens


def unique_evidence(items: Iterable[EvidenceSnippet]) -> List[EvidenceSnippet]:
    seen = set()
    unique: List[EvidenceSnippet] = []
    for item in items:
        key = (item.signal, item.start, item.end, item.snippet)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique
