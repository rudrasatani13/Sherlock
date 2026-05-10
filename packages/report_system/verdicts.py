"""Launch readiness verdict selection for Phase 18 web reports."""
from __future__ import annotations

from typing import Any, Iterable

from packages.findings_system.statuses import normalize_status

from .models import (
    LaunchReadinessVerdict,
    SecurityScore,
    VERDICT_HIGH_RISK_DO_NOT_LAUNCH,
    VERDICT_INCONCLUSIVE,
    VERDICT_MANUAL_REVIEW_REQUIRED,
    VERDICT_NEEDS_FIXES_BEFORE_LAUNCH,
    VERDICT_READY_WITH_LOW_RISK,
)


ACTIVE_STATUSES = {"open", "accepted_risk", "needs_review"}


def select_launch_readiness_verdict(
    findings: Iterable[Any],
    security_score: SecurityScore,
    *,
    tested_categories: Iterable[Any] | None = None,
    not_tested: Iterable[str] | None = None,
) -> LaunchReadinessVerdict:
    """Select a careful, non-overclaiming launch readiness verdict."""
    finding_list = list(findings or [])
    tested = list(tested_categories or [])
    not_tested_list = [item for item in (not_tested or []) if str(item).strip()]

    if not tested:
        return LaunchReadinessVerdict(
            verdict=VERDICT_INCONCLUSIVE,
            label="Inconclusive",
            summary="Launch readiness cannot be assessed because no tested categories were provided.",
            recommended_action="Define tested scope, run the approved test categories, and review evidence before launch decisions.",
        )

    active_critical = any(_active(finding) and _severity(finding) == "critical" for finding in finding_list)
    if active_critical:
        return LaunchReadinessVerdict(
            verdict=VERDICT_HIGH_RISK_DO_NOT_LAUNCH,
            label="High risk, do not launch",
            summary="At least one active Critical finding is present in the tested scope.",
            recommended_action="Fix and retest Critical findings before broad launch.",
        )

    active_high = any(_active(finding) and _severity(finding) == "high" for finding in finding_list)
    active_medium = any(_active(finding) and _severity(finding) == "medium" for finding in finding_list)
    if active_high or security_score.score < 70:
        return LaunchReadinessVerdict(
            verdict=VERDICT_NEEDS_FIXES_BEFORE_LAUNCH,
            label="Needs fixes before launch",
            summary="The tested scope includes material findings that should be remediated before broad release.",
            recommended_action="Prioritize High findings, then retest the original scenarios and update the report status.",
        )

    needs_review = any(
        _status(finding) == "needs_review" or bool(_get(finding, "manual_review_required", False))
        for finding in finding_list
    )
    if needs_review:
        return LaunchReadinessVerdict(
            verdict=VERDICT_MANUAL_REVIEW_REQUIRED,
            label="Manual review required",
            summary="One or more findings require human review before a launch recommendation should be treated as final.",
            recommended_action="Review evidence quality, confirm impact, and update finding status before launch decisions.",
        )

    if active_medium:
        return LaunchReadinessVerdict(
            verdict=VERDICT_NEEDS_FIXES_BEFORE_LAUNCH,
            label="Needs fixes before launch",
            summary="Open Medium findings remain in the tested scope.",
            recommended_action="Fix or accept the documented risk, then retest where relevant.",
        )

    if security_score.score >= 80:
        summary = "No active Critical, High, or Medium findings remain in the tested scope."
        if not_tested_list:
            summary += " Categories outside the documented scope may still contain risk."
        return LaunchReadinessVerdict(
            verdict=VERDICT_READY_WITH_LOW_RISK,
            label="Ready with low observed launch risk",
            summary=summary,
            recommended_action="Launch decisions should still account for untested scope, integrations, and operational monitoring.",
        )

    return LaunchReadinessVerdict(
        verdict=VERDICT_INCONCLUSIVE,
        label="Inconclusive",
        summary="The available evidence does not support a clear launch-readiness decision.",
        recommended_action="Expand tested scope, review ambiguous findings, and retest after remediation.",
    )


def _active(finding: Any) -> bool:
    return _status(finding) in ACTIVE_STATUSES


def _status(finding: Any) -> str:
    try:
        return normalize_status(str(_get(finding, "status", "needs_review") or "needs_review"))
    except ValueError:
        return "needs_review"


def _severity(finding: Any) -> str:
    return str(_get(finding, "severity", "informational") or "informational").strip().lower()


def _get(item: Any, name: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)
