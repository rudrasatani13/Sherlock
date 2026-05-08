"""Plan/tier placeholder definitions for Sherlock.

Defines future access tiers with scan type availability, monthly limits,
and feature gating. This is a placeholder matrix only — billing, Stripe,
and real plan enforcement are NOT implemented.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional


# ---------------------------------------------------------------------------
# Plan tier constants
# ---------------------------------------------------------------------------

class PlanTierName:
    FREE = "free"
    LAUNCH_SCAN = "launch_scan"
    BUILDER = "builder"
    STARTUP = "startup"
    MANUAL_AUDIT = "manual_audit"

    ALL: FrozenSet[str] = frozenset({
        "free",
        "launch_scan",
        "builder",
        "startup",
        "manual_audit",
    })


# ---------------------------------------------------------------------------
# Plan tier definition
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PlanTier:
    """Placeholder plan/tier definition. Not connected to billing."""
    tier: str
    display_name: str
    description: str
    allowed_scan_types: FrozenSet[str]
    monthly_scan_limit: int
    max_projects: int
    retest_allowance: int
    pdf_export_available: bool
    web_report_available: bool
    manual_review_available: bool
    enabled: bool
    billing_placeholder: str  # "free", "future_paid", "custom_quote"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tier": self.tier,
            "display_name": self.display_name,
            "description": self.description,
            "allowed_scan_types": sorted(self.allowed_scan_types),
            "monthly_scan_limit": self.monthly_scan_limit,
            "max_projects": self.max_projects,
            "retest_allowance": self.retest_allowance,
            "pdf_export_available": self.pdf_export_available,
            "web_report_available": self.web_report_available,
            "manual_review_available": self.manual_review_available,
            "enabled": self.enabled,
            "billing_placeholder": self.billing_placeholder,
        }


# ---------------------------------------------------------------------------
# V0 plan tier definitions — NOT connected to billing
# ---------------------------------------------------------------------------

PLAN_TIERS: Dict[str, PlanTier] = {
    PlanTierName.FREE: PlanTier(
        tier=PlanTierName.FREE,
        display_name="Free",
        description="Limited demo/trial tier with quick scans only. No billing required.",
        allowed_scan_types=frozenset({"quick_scan"}),
        monthly_scan_limit=3,
        max_projects=1,
        retest_allowance=0,
        pdf_export_available=False,
        web_report_available=False,
        manual_review_available=False,
        enabled=False,  # Not active until billing gates exist
        billing_placeholder="free",
    ),
    PlanTierName.LAUNCH_SCAN: PlanTier(
        tier=PlanTierName.LAUNCH_SCAN,
        display_name="Launch Scan",
        description="Single launch-readiness scan for teams shipping their first AI app.",
        allowed_scan_types=frozenset({"quick_scan", "standard_scan", "retest_scan"}),
        monthly_scan_limit=5,
        max_projects=2,
        retest_allowance=2,
        pdf_export_available=False,
        web_report_available=True,
        manual_review_available=False,
        enabled=False,
        billing_placeholder="future_paid",
    ),
    PlanTierName.BUILDER: PlanTier(
        tier=PlanTierName.BUILDER,
        display_name="Builder",
        description="Ongoing AI security testing for growing teams with multiple projects.",
        allowed_scan_types=frozenset({"quick_scan", "standard_scan", "deep_scan", "retest_scan"}),
        monthly_scan_limit=20,
        max_projects=5,
        retest_allowance=10,
        pdf_export_available=True,
        web_report_available=True,
        manual_review_available=False,
        enabled=False,
        billing_placeholder="future_paid",
    ),
    PlanTierName.STARTUP: PlanTier(
        tier=PlanTierName.STARTUP,
        display_name="Startup",
        description="Full platform access with deep scans, expanded project limits, and PDF export.",
        allowed_scan_types=frozenset({"quick_scan", "standard_scan", "deep_scan", "retest_scan"}),
        monthly_scan_limit=50,
        max_projects=15,
        retest_allowance=25,
        pdf_export_available=True,
        web_report_available=True,
        manual_review_available=False,
        enabled=False,
        billing_placeholder="future_paid",
    ),
    PlanTierName.MANUAL_AUDIT: PlanTier(
        tier=PlanTierName.MANUAL_AUDIT,
        display_name="Manual Audit",
        description="Custom engagement with expert-led audit, assisted scanning, and manual review. Quote-based pricing.",
        allowed_scan_types=frozenset({"quick_scan", "standard_scan", "deep_scan", "manual_audit_assisted", "retest_scan"}),
        monthly_scan_limit=100,
        max_projects=25,
        retest_allowance=50,
        pdf_export_available=True,
        web_report_available=True,
        manual_review_available=True,
        enabled=False,
        billing_placeholder="custom_quote",
    ),
}


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def get_plan_tier(name: str) -> Optional[PlanTier]:
    """Return the PlanTier for a given tier name, or None."""
    return PLAN_TIERS.get(name)


def get_plan_tier_names() -> List[str]:
    """Return sorted list of all defined plan tier names."""
    return sorted(PLAN_TIERS.keys())
