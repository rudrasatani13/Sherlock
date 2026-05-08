from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError, build_metadata
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.scans import (
    ScanQueueContract,
    ScanTypeEntry,
    ScansModuleStatus,
    PlanTierEntry,
)

router = APIRouter(prefix="/scans", tags=["scans"])


def _build_scan_types() -> list[dict]:
    """Build scan type entries from the Phase 16 scan_limits package."""
    try:
        from packages.scan_limits.scan_types import SCAN_TYPES
        entries = []
        for name, config in sorted(SCAN_TYPES.items()):
            entries.append(ScanTypeEntry(
                scan_type=config.scan_type,
                display_name=config.display_name,
                description=config.description,
                max_tests=config.max_tests,
                timeout_seconds=config.timeout_seconds,
                max_concurrency=config.max_concurrency,
                max_response_chars_per_test=config.max_response_chars_per_test,
                included_categories=sorted(config.included_categories),
                requires_verified_target=config.requires_verified_target,
                requires_manual_review=config.requires_manual_review,
                report_level=config.report_level,
                enabled=config.enabled,
                future_plan_availability=list(config.future_plan_availability),
            ))
        return [serialize_model(e) for e in entries]
    except ImportError:
        return []


def _build_plan_tiers() -> list[dict]:
    """Build plan tier entries from the Phase 16 scan_limits package."""
    try:
        from packages.scan_limits.plans import PLAN_TIERS
        entries = []
        for name, tier in sorted(PLAN_TIERS.items()):
            entries.append(PlanTierEntry(
                tier=tier.tier,
                display_name=tier.display_name,
                description=tier.description,
                allowed_scan_types=sorted(tier.allowed_scan_types),
                monthly_scan_limit=tier.monthly_scan_limit,
                max_projects=tier.max_projects,
                retest_allowance=tier.retest_allowance,
                pdf_export_available=tier.pdf_export_available,
                web_report_available=tier.web_report_available,
                enabled=tier.enabled,
                billing_placeholder=tier.billing_placeholder,
            ))
        return [serialize_model(e) for e in entries]
    except ImportError:
        return []


@router.get("", response_model=ApiResponse)
def scans_placeholder() -> ApiResponse:
    module_status = ScansModuleStatus(
        future_capabilities=[
            "scan job creation (authenticated + verified targets only)",
            "scan job status queries",
            "scan job cancellation",
            "queue worker handoff",
            "worker result ingestion",
            "scan type selection",
            "scan limit enforcement",
        ],
        disabled_capabilities=[
            "public scan creation",
            "production queue deployment",
            "active scan persistence",
            "ownership verification bypasses",
            "scanner execution from API routes",
            "real network scanning",
            "billing enforcement",
        ],
    )
    queue_contract = ScanQueueContract()
    details = serialize_model(module_status)
    details["queue_contract"] = serialize_model(queue_contract)
    details["scan_types"] = _build_scan_types()
    details["plan_tiers"] = _build_plan_tiers()
    raise NotImplementedApiError("scans", details)


@router.get("/types", response_model=ApiResponse)
def scan_types_list() -> ApiResponse:
    """Return all defined scan types and their limits.

    This is a static/safe endpoint — it does not create scan jobs or
    trigger workers. Phase 16 foundation only.
    """
    scan_types = _build_scan_types()
    return ApiResponse(
        success=True,
        data={
            "scan_types": scan_types,
            "total": len(scan_types),
            "phase": "Phase 16 scan types and limits foundation",
            "note": "Scan types define bounded modes with limits. Public scan execution is not implemented.",
        },
        error=None,
        metadata=build_metadata(),
    )


@router.get("/limits", response_model=ApiResponse)
def scan_limits_info() -> ApiResponse:
    """Return current scan limits, plan tier info, and category matrix.

    This is a static/safe endpoint. Phase 16 foundation only.
    """
    scan_types = _build_scan_types()
    plan_tiers = _build_plan_tiers()

    try:
        from packages.scan_limits.categories import ALL_CATEGORIES, CATEGORY_DISPLAY_NAMES
        categories = [
            {"id": cat, "display_name": CATEGORY_DISPLAY_NAMES.get(cat, cat)}
            for cat in sorted(ALL_CATEGORIES)
        ]
    except ImportError:
        categories = []

    return ApiResponse(
        success=True,
        data={
            "scan_types": scan_types,
            "plan_tiers": plan_tiers,
            "categories": categories,
            "phase": "Phase 16 scan types and limits foundation",
            "security_notes": {
                "every_scan_bounded": True,
                "verified_target_required": True,
                "unbounded_execution_forbidden": True,
                "secrets_in_payloads_rejected": True,
                "billing_enforcement_active": False,
                "public_scan_execution_active": False,
            },
            "note": "Limits and plan tiers are placeholders. Billing, Stripe, and production enforcement are not implemented.",
        },
        error=None,
        metadata=build_metadata(),
    )
