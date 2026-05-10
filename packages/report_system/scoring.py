"""Conservative security score helper for Phase 18 web reports."""
from __future__ import annotations

from typing import Any, Iterable, List

from packages.findings_system.severity import CONFIDENCE_RANK, SEVERITY_RANK, normalize_confidence, normalize_severity
from packages.findings_system.statuses import normalize_status

from .models import SecurityScore


BASE_SCORE = 92
NO_FINDINGS_SCORE = 88

SEVERITY_PENALTIES: dict[str, int] = {
    "critical": 34,
    "high": 19,
    "medium": 8,
    "low": 3,
    "informational": 1,
}

CONFIDENCE_MULTIPLIERS: dict[str, float] = {
    "high": 1.0,
    "medium": 0.85,
    "low": 0.65,
}

ACTIVE_STATUSES = {"open", "accepted_risk", "needs_review"}


def calculate_security_score(findings: Iterable[Any]) -> SecurityScore:
    """Calculate a bounded 0-100 score from report findings.

    The score is intentionally conservative. No findings does not mean 100,
    active Critical/High findings cap the score, and needs-review findings
    reduce confidence in the score.
    """
    normalized = list(findings or [])
    limitations = [
        "No findings observed does not automatically mean a 100 score.",
        "The score reflects only the tested scope, categories, evidence, and review state in this report.",
        "Needs-review or inconclusive evidence caps score confidence until a human review completes.",
    ]
    if not normalized:
        return SecurityScore(
            score=NO_FINDINGS_SCORE,
            explanation="No report findings were provided. The score is capped because untested categories and hidden risks may still exist.",
            limitations=limitations,
        )

    penalty = 0.0
    active_severities: List[str] = []
    needs_review_severities: List[str] = []

    for finding in normalized:
        status = _status(finding)
        severity = _severity(finding)
        confidence = _confidence(finding)

        if status == "false_positive":
            continue

        multiplier = CONFIDENCE_MULTIPLIERS[confidence]
        status_multiplier = 0.2 if status == "fixed" else 1.0
        penalty += SEVERITY_PENALTIES[severity] * multiplier * status_multiplier

        if status in ACTIVE_STATUSES:
            active_severities.append(severity)
        if status == "needs_review" or bool(_get(finding, "manual_review_required", False)):
            needs_review_severities.append(severity)

    score = int(round(BASE_SCORE - penalty))
    score = max(0, min(100, score))

    if "critical" in active_severities:
        score = min(score, 44)
    elif "high" in active_severities:
        score = min(score, 68)
    elif "medium" in active_severities:
        score = min(score, 82)

    if any(severity in {"critical", "high"} for severity in needs_review_severities):
        score = min(score, 60)
    elif needs_review_severities:
        score = min(score, 76)

    explanation = (
        "Score starts below 100 and subtracts weighted penalties for severity, confidence, and review state. "
        "False positives do not reduce score; fixed findings retain only a small historical penalty."
    )
    return SecurityScore(score=score, explanation=explanation, limitations=limitations)


def _severity(finding: Any) -> str:
    return normalize_severity(str(_get(finding, "severity", "informational") or "informational"))


def _confidence(finding: Any) -> str:
    return normalize_confidence(str(_get(finding, "confidence", "low") or "low"))


def _status(finding: Any) -> str:
    try:
        return normalize_status(str(_get(finding, "status", "needs_review") or "needs_review"))
    except ValueError:
        return "needs_review"


def _get(item: Any, name: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)
