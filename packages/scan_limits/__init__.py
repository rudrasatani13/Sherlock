"""Scan type definitions, limit validation, and plan/tier placeholders for Sherlock.

Phase 16 foundation — defines bounded scan modes, category inclusion rules,
plan-aware limits, and validation helpers. Does not implement billing, real
scan execution, or production enforcement.
"""
from .scan_types import (
    SCAN_TYPES,
    ScanType,
    ScanTypeConfig,
    get_scan_type,
    get_scan_type_names,
    is_scan_type_enabled,
)
from .categories import (
    ALL_CATEGORIES,
    CATEGORY_DISPLAY_NAMES,
    get_categories_for_scan_type,
)
from .plans import (
    PLAN_TIERS,
    PlanTier,
    get_plan_tier,
    get_plan_tier_names,
)
from .validators import (
    ScanLimitValidationResult,
    validate_scan_request,
    validate_scan_type_exists,
    validate_scan_type_enabled,
    validate_categories_allowed,
    validate_max_tests,
    validate_timeout,
    validate_concurrency,
    validate_target_verified,
    validate_manual_audit_guard,
    validate_retest_categories,
    validate_payload_no_secrets,
)

__all__ = [
    "ALL_CATEGORIES",
    "CATEGORY_DISPLAY_NAMES",
    "PLAN_TIERS",
    "PlanTier",
    "SCAN_TYPES",
    "ScanLimitValidationResult",
    "ScanType",
    "ScanTypeConfig",
    "get_categories_for_scan_type",
    "get_plan_tier",
    "get_plan_tier_names",
    "get_scan_type",
    "get_scan_type_names",
    "is_scan_type_enabled",
    "validate_categories_allowed",
    "validate_concurrency",
    "validate_manual_audit_guard",
    "validate_max_tests",
    "validate_payload_no_secrets",
    "validate_retest_categories",
    "validate_scan_request",
    "validate_scan_type_enabled",
    "validate_scan_type_exists",
    "validate_target_verified",
    "validate_timeout",
]
