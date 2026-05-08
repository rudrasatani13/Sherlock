"""Finding status constants for Phase 17."""
from __future__ import annotations


STATUS_OPEN = "open"
STATUS_FIXED = "fixed"
STATUS_ACCEPTED_RISK = "accepted_risk"
STATUS_FALSE_POSITIVE = "false_positive"
STATUS_NEEDS_REVIEW = "needs_review"

STATUSES: tuple[str, ...] = (
    STATUS_OPEN,
    STATUS_FIXED,
    STATUS_ACCEPTED_RISK,
    STATUS_FALSE_POSITIVE,
    STATUS_NEEDS_REVIEW,
)

# Future statuses are documented for contract planning only. Phase 17 finalized
# findings normalize into STATUSES above.
FUTURE_STATUSES: tuple[str, ...] = (
    "inconclusive",
    "duplicate",
    "retest_required",
)

STATUS_DISPLAY_NAMES: dict[str, str] = {
    STATUS_OPEN: "Open",
    STATUS_FIXED: "Fixed",
    STATUS_ACCEPTED_RISK: "Accepted risk",
    STATUS_FALSE_POSITIVE: "False positive",
    STATUS_NEEDS_REVIEW: "Needs review",
}

STATUS_ALIASES: dict[str, str] = {
    "needs_manual_review": STATUS_NEEDS_REVIEW,
    "manual_review_required": STATUS_NEEDS_REVIEW,
    "review": STATUS_NEEDS_REVIEW,
    "accepted risk": STATUS_ACCEPTED_RISK,
    "false positive": STATUS_FALSE_POSITIVE,
}


def normalize_status(value: str | None, default: str = STATUS_NEEDS_REVIEW) -> str:
    """Return one of the five normalized Phase 17 statuses."""
    normalized = (value or "").strip().lower().replace("-", "_")
    normalized = STATUS_ALIASES.get(normalized, normalized)
    normalized = normalized.replace(" ", "_")
    if not normalized:
        normalized = default
    if normalized not in STATUSES:
        raise ValueError(f"unsupported finding status: {value}")
    return normalized


def is_valid_status(value: str | None) -> bool:
    try:
        normalize_status(value)
    except ValueError:
        return False
    return True
