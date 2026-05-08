"""Severity and confidence helpers for the Phase 17 findings system."""
from __future__ import annotations

from typing import Iterable


SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"
SEVERITY_INFORMATIONAL = "informational"

SEVERITIES: tuple[str, ...] = (
    SEVERITY_CRITICAL,
    SEVERITY_HIGH,
    SEVERITY_MEDIUM,
    SEVERITY_LOW,
    SEVERITY_INFORMATIONAL,
)

SEVERITY_RANK: dict[str, int] = {
    SEVERITY_INFORMATIONAL: 1,
    SEVERITY_LOW: 2,
    SEVERITY_MEDIUM: 3,
    SEVERITY_HIGH: 4,
    SEVERITY_CRITICAL: 5,
}

CONFIDENCE_HIGH = "high"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_LOW = "low"

CONFIDENCES: tuple[str, ...] = (
    CONFIDENCE_HIGH,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_LOW,
)

CONFIDENCE_RANK: dict[str, int] = {
    CONFIDENCE_LOW: 1,
    CONFIDENCE_MEDIUM: 2,
    CONFIDENCE_HIGH: 3,
}


def normalize_severity(value: str | None, default: str = SEVERITY_INFORMATIONAL) -> str:
    """Return a supported Phase 3/17 severity value."""
    normalized = (value or "").strip().lower().replace(" ", "_").replace("-", "_")
    if normalized in {"", "none", "unknown", "not_assigned_by_scanner_engine"}:
        normalized = default
    if normalized not in SEVERITY_RANK:
        raise ValueError(f"unsupported severity: {value}")
    return normalized


def normalize_confidence(value: str | None, default: str = CONFIDENCE_LOW) -> str:
    """Return a supported Phase 3/17 confidence value."""
    normalized = (value or "").strip().lower().replace(" ", "_").replace("-", "_")
    if normalized in {"", "none", "unknown"}:
        normalized = default
    if normalized not in CONFIDENCE_RANK:
        raise ValueError(f"unsupported confidence: {value}")
    return normalized


def strongest_severity(values: Iterable[str | None]) -> str:
    """Return the highest ranked severity from *values*."""
    normalized = [normalize_severity(value) for value in values]
    if not normalized:
        return SEVERITY_INFORMATIONAL
    return max(normalized, key=lambda item: SEVERITY_RANK[item])


def strongest_confidence(values: Iterable[str | None]) -> str:
    """Return the highest ranked confidence from *values*."""
    normalized = [normalize_confidence(value) for value in values]
    if not normalized:
        return CONFIDENCE_LOW
    return max(normalized, key=lambda item: CONFIDENCE_RANK[item])


def severity_sort_value(value: str) -> int:
    """Return a descending sort value for severity."""
    return -SEVERITY_RANK[normalize_severity(value)]


def confidence_sort_value(value: str) -> int:
    """Return a descending sort value for confidence."""
    return -CONFIDENCE_RANK[normalize_confidence(value)]
