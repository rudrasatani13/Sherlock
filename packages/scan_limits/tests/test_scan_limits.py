"""Tests for Phase 16 scan types, limits, categories, plans, and validation helpers."""
from __future__ import annotations

import unittest
from typing import List

from packages.scan_limits.categories import (
    ALL_CATEGORIES,
    CATEGORY_DISPLAY_NAMES,
    QUICK_CATEGORIES,
    STANDARD_CATEGORIES,
    DEEP_CATEGORIES,
    SCAN_TYPE_CATEGORIES,
    get_categories_for_scan_type,
    is_category_valid,
)
from packages.scan_limits.scan_types import (
    SCAN_TYPES,
    ScanType,
    ScanTypeConfig,
    ReportLevel,
    get_scan_type,
    get_scan_type_names,
    is_scan_type_enabled,
)
from packages.scan_limits.plans import (
    PLAN_TIERS,
    PlanTier,
    PlanTierName,
    get_plan_tier,
    get_plan_tier_names,
)
from packages.scan_limits.validators import (
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


# -------------------------------------------------------------------------
# Category tests
# -------------------------------------------------------------------------

class CategoryRegistryTests(unittest.TestCase):
    def test_all_categories_count(self) -> None:
        self.assertEqual(len(ALL_CATEGORIES), 8)

    def test_known_categories_present(self) -> None:
        expected = [
            "prompt_injection", "system_prompt_leakage", "sensitive_data_leakage",
            "rag_data_leakage", "indirect_prompt_injection", "tool_function_abuse",
            "unsafe_output_handling", "cost_abuse",
        ]
        for cat in expected:
            self.assertIn(cat, ALL_CATEGORIES, f"Missing category: {cat}")

    def test_display_names_cover_all_categories(self) -> None:
        for cat in ALL_CATEGORIES:
            self.assertIn(cat, CATEGORY_DISPLAY_NAMES, f"Missing display name for: {cat}")

    def test_quick_categories_are_subset(self) -> None:
        self.assertTrue(QUICK_CATEGORIES.issubset(ALL_CATEGORIES))
        self.assertIn("prompt_injection", QUICK_CATEGORIES)
        self.assertNotIn("rag_data_leakage", QUICK_CATEGORIES)

    def test_standard_categories_are_subset(self) -> None:
        self.assertTrue(STANDARD_CATEGORIES.issubset(ALL_CATEGORIES))
        self.assertIn("rag_data_leakage", STANDARD_CATEGORIES)
        self.assertNotIn("indirect_prompt_injection", STANDARD_CATEGORIES)

    def test_deep_categories_equal_all(self) -> None:
        self.assertEqual(DEEP_CATEGORIES, ALL_CATEGORIES)

    def test_get_categories_for_scan_type(self) -> None:
        quick_cats = get_categories_for_scan_type("quick_scan")
        self.assertIsInstance(quick_cats, list)
        self.assertTrue(len(quick_cats) > 0)
        self.assertEqual(quick_cats, sorted(quick_cats))  # sorted

    def test_get_categories_unknown_type(self) -> None:
        self.assertEqual(get_categories_for_scan_type("nonexistent"), [])

    def test_is_category_valid(self) -> None:
        self.assertTrue(is_category_valid("prompt_injection"))
        self.assertFalse(is_category_valid("fake_category"))

    def test_scan_type_category_mapping_complete(self) -> None:
        for scan_type in ScanType.ALL:
            self.assertIn(scan_type, SCAN_TYPE_CATEGORIES, f"Missing category mapping for: {scan_type}")


# -------------------------------------------------------------------------
# Scan type tests
# -------------------------------------------------------------------------

class ScanTypeTests(unittest.TestCase):
    def test_all_five_scan_types_defined(self) -> None:
        self.assertEqual(len(SCAN_TYPES), 5)
        expected = {"quick_scan", "standard_scan", "deep_scan", "manual_audit_assisted", "retest_scan"}
        self.assertEqual(set(SCAN_TYPES.keys()), expected)

    def test_scan_type_all_constant(self) -> None:
        self.assertEqual(ScanType.ALL, set(SCAN_TYPES.keys()))

    def test_quick_scan_limits(self) -> None:
        config = get_scan_type("quick_scan")
        self.assertIsNotNone(config)
        self.assertEqual(config.max_tests, 10)
        self.assertEqual(config.timeout_seconds, 120)
        self.assertEqual(config.max_concurrency, 1)
        self.assertEqual(config.max_response_chars_per_test, 4000)
        self.assertTrue(config.requires_verified_target)
        self.assertFalse(config.requires_manual_review)
        self.assertFalse(config.allow_rag_tests)
        self.assertFalse(config.allow_tool_tests)
        self.assertEqual(config.report_level, ReportLevel.SUMMARY)
        self.assertTrue(config.enabled)

    def test_standard_scan_limits(self) -> None:
        config = get_scan_type("standard_scan")
        self.assertIsNotNone(config)
        self.assertEqual(config.max_tests, 50)
        self.assertEqual(config.timeout_seconds, 600)
        self.assertEqual(config.max_concurrency, 2)
        self.assertTrue(config.allow_rag_tests)
        self.assertFalse(config.allow_tool_tests)
        self.assertTrue(config.allow_cost_abuse_tests)
        self.assertEqual(config.report_level, ReportLevel.STANDARD)
        self.assertTrue(config.enabled)

    def test_deep_scan_limits(self) -> None:
        config = get_scan_type("deep_scan")
        self.assertIsNotNone(config)
        self.assertEqual(config.max_tests, 150)
        self.assertEqual(config.timeout_seconds, 1800)
        self.assertEqual(config.max_concurrency, 3)
        self.assertTrue(config.allow_rag_tests)
        self.assertTrue(config.allow_tool_tests)
        self.assertTrue(config.allow_indirect_injection_tests)
        self.assertEqual(config.report_level, ReportLevel.DETAILED)
        self.assertFalse(config.enabled)  # Gated until paid plan

    def test_manual_audit_assisted_limits(self) -> None:
        config = get_scan_type("manual_audit_assisted")
        self.assertIsNotNone(config)
        self.assertEqual(config.max_tests, 250)
        self.assertEqual(config.timeout_seconds, 3600)
        self.assertTrue(config.requires_manual_review)
        self.assertFalse(config.enabled)
        self.assertEqual(config.report_level, ReportLevel.MANUAL_REVIEW)

    def test_retest_scan_limits(self) -> None:
        config = get_scan_type("retest_scan")
        self.assertIsNotNone(config)
        self.assertEqual(config.max_tests, 20)
        self.assertEqual(config.timeout_seconds, 300)
        self.assertEqual(config.max_concurrency, 1)
        self.assertTrue(config.targeted_categories_only)
        self.assertEqual(config.report_level, ReportLevel.RETEST)
        self.assertTrue(config.enabled)

    def test_get_scan_type_unknown(self) -> None:
        self.assertIsNone(get_scan_type("nonexistent"))

    def test_get_scan_type_names(self) -> None:
        names = get_scan_type_names()
        self.assertEqual(names, sorted(names))
        self.assertEqual(len(names), 5)

    def test_is_scan_type_enabled(self) -> None:
        self.assertTrue(is_scan_type_enabled("quick_scan"))
        self.assertTrue(is_scan_type_enabled("standard_scan"))
        self.assertFalse(is_scan_type_enabled("deep_scan"))
        self.assertFalse(is_scan_type_enabled("manual_audit_assisted"))
        self.assertTrue(is_scan_type_enabled("retest_scan"))
        self.assertFalse(is_scan_type_enabled("fake"))

    def test_every_scan_type_requires_verified_target(self) -> None:
        for name, config in SCAN_TYPES.items():
            self.assertTrue(
                config.requires_verified_target,
                f"Scan type '{name}' must require verified target",
            )

    def test_scan_type_config_serializes(self) -> None:
        for name, config in SCAN_TYPES.items():
            data = config.to_dict()
            self.assertEqual(data["scan_type"], name)
            self.assertIn("max_tests", data)
            self.assertIn("included_categories", data)
            self.assertIsInstance(data["included_categories"], list)

    def test_no_scan_type_exceeds_absolute_bounds(self) -> None:
        for name, config in SCAN_TYPES.items():
            self.assertLessEqual(config.max_tests, 500, f"{name} max_tests too high")
            self.assertLessEqual(config.timeout_seconds, 7200, f"{name} timeout too high")
            self.assertLessEqual(config.max_concurrency, 10, f"{name} concurrency too high")


# -------------------------------------------------------------------------
# Plan tier tests
# -------------------------------------------------------------------------

class PlanTierTests(unittest.TestCase):
    def test_all_five_plan_tiers_defined(self) -> None:
        self.assertEqual(len(PLAN_TIERS), 5)
        expected = {"free", "launch_scan", "builder", "startup", "manual_audit"}
        self.assertEqual(set(PLAN_TIERS.keys()), expected)

    def test_plan_tier_all_constant(self) -> None:
        self.assertEqual(PlanTierName.ALL, set(PLAN_TIERS.keys()))

    def test_free_tier_limits(self) -> None:
        tier = get_plan_tier("free")
        self.assertIsNotNone(tier)
        self.assertEqual(tier.monthly_scan_limit, 3)
        self.assertEqual(tier.max_projects, 1)
        self.assertEqual(tier.retest_allowance, 0)
        self.assertFalse(tier.pdf_export_available)
        self.assertFalse(tier.web_report_available)
        self.assertIn("quick_scan", tier.allowed_scan_types)
        self.assertNotIn("deep_scan", tier.allowed_scan_types)

    def test_manual_audit_tier_has_all_scan_types(self) -> None:
        tier = get_plan_tier("manual_audit")
        self.assertIsNotNone(tier)
        for scan_type in ScanType.ALL:
            self.assertIn(scan_type, tier.allowed_scan_types)

    def test_no_plan_tier_is_enabled(self) -> None:
        for name, tier in PLAN_TIERS.items():
            self.assertFalse(tier.enabled, f"Plan tier '{name}' should not be enabled — billing is not implemented")

    def test_get_plan_tier_unknown(self) -> None:
        self.assertIsNone(get_plan_tier("nonexistent"))

    def test_get_plan_tier_names(self) -> None:
        names = get_plan_tier_names()
        self.assertEqual(names, sorted(names))

    def test_plan_tier_serializes(self) -> None:
        for name, tier in PLAN_TIERS.items():
            data = tier.to_dict()
            self.assertEqual(data["tier"], name)
            self.assertIn("monthly_scan_limit", data)
            self.assertIsInstance(data["allowed_scan_types"], list)

    def test_scan_type_availability_matrix(self) -> None:
        # Each enabled scan type should appear in at least one plan
        for scan_type_name, scan_config in SCAN_TYPES.items():
            found = False
            for tier_name, tier in PLAN_TIERS.items():
                if scan_type_name in tier.allowed_scan_types:
                    found = True
                    break
            self.assertTrue(found, f"Scan type '{scan_type_name}' not in any plan tier")


# -------------------------------------------------------------------------
# Validator tests
# -------------------------------------------------------------------------

class ScanTypeExistsTests(unittest.TestCase):
    def test_valid_type(self) -> None:
        self.assertIsNone(validate_scan_type_exists("quick_scan"))
        self.assertIsNone(validate_scan_type_exists("standard_scan"))

    def test_invalid_type(self) -> None:
        err = validate_scan_type_exists("nonexistent")
        self.assertIsNotNone(err)
        self.assertIn("Unknown scan type", err)


class ScanTypeEnabledTests(unittest.TestCase):
    def test_enabled_type(self) -> None:
        self.assertIsNone(validate_scan_type_enabled("quick_scan"))

    def test_disabled_type(self) -> None:
        err = validate_scan_type_enabled("deep_scan")
        self.assertIsNotNone(err)
        self.assertIn("disabled", err)

    def test_unknown_type(self) -> None:
        err = validate_scan_type_enabled("nonexistent")
        self.assertIsNotNone(err)


class TargetVerifiedTests(unittest.TestCase):
    def test_verified_passes(self) -> None:
        self.assertIsNone(validate_target_verified("quick_scan", "verified"))

    def test_unverified_blocked(self) -> None:
        err = validate_target_verified("quick_scan", "unverified")
        self.assertIsNotNone(err)
        self.assertIn("verified", err)

    def test_pending_blocked(self) -> None:
        err = validate_target_verified("standard_scan", "pending")
        self.assertIsNotNone(err)

    def test_manual_audit_with_override(self) -> None:
        self.assertIsNone(
            validate_target_verified("manual_audit_assisted", "pending", manual_authorization_override=True)
        )

    def test_manual_audit_without_override(self) -> None:
        err = validate_target_verified("manual_audit_assisted", "unverified")
        self.assertIsNotNone(err)


class CategoriesAllowedTests(unittest.TestCase):
    def test_valid_quick_categories(self) -> None:
        self.assertIsNone(validate_categories_allowed("quick_scan", ["prompt_injection"]))

    def test_disallowed_category_for_quick(self) -> None:
        err = validate_categories_allowed("quick_scan", ["rag_data_leakage"])
        self.assertIsNotNone(err)
        self.assertIn("not included", err)

    def test_unknown_category(self) -> None:
        err = validate_categories_allowed("standard_scan", ["fake_category"])
        self.assertIsNotNone(err)
        self.assertIn("Unknown categories", err)

    def test_empty_categories_passes(self) -> None:
        self.assertIsNone(validate_categories_allowed("standard_scan", []))

    def test_deep_scan_all_categories(self) -> None:
        self.assertIsNone(validate_categories_allowed("deep_scan", list(ALL_CATEGORIES)))


class MaxTestsTests(unittest.TestCase):
    def test_within_limit(self) -> None:
        self.assertIsNone(validate_max_tests("quick_scan", 5))

    def test_at_limit(self) -> None:
        self.assertIsNone(validate_max_tests("quick_scan", 10))

    def test_exceeds_limit(self) -> None:
        err = validate_max_tests("quick_scan", 11)
        self.assertIsNotNone(err)
        self.assertIn("exceeds limit", err)

    def test_zero_rejected(self) -> None:
        err = validate_max_tests("quick_scan", 0)
        self.assertIsNotNone(err)

    def test_negative_rejected(self) -> None:
        err = validate_max_tests("quick_scan", -1)
        self.assertIsNotNone(err)

    def test_standard_limit(self) -> None:
        self.assertIsNone(validate_max_tests("standard_scan", 50))
        err = validate_max_tests("standard_scan", 51)
        self.assertIsNotNone(err)

    def test_deep_limit(self) -> None:
        self.assertIsNone(validate_max_tests("deep_scan", 150))
        err = validate_max_tests("deep_scan", 151)
        self.assertIsNotNone(err)


class TimeoutTests(unittest.TestCase):
    def test_within_limit(self) -> None:
        self.assertIsNone(validate_timeout("quick_scan", 60))

    def test_exceeds_limit(self) -> None:
        err = validate_timeout("quick_scan", 121)
        self.assertIsNotNone(err)
        self.assertIn("exceeds limit", err)

    def test_standard_timeout(self) -> None:
        self.assertIsNone(validate_timeout("standard_scan", 600))
        err = validate_timeout("standard_scan", 601)
        self.assertIsNotNone(err)


class ConcurrencyTests(unittest.TestCase):
    def test_within_limit(self) -> None:
        self.assertIsNone(validate_concurrency("quick_scan", 1))

    def test_exceeds_limit(self) -> None:
        err = validate_concurrency("quick_scan", 2)
        self.assertIsNotNone(err)
        self.assertIn("exceeds limit", err)

    def test_deep_concurrency(self) -> None:
        self.assertIsNone(validate_concurrency("deep_scan", 3))
        err = validate_concurrency("deep_scan", 4)
        self.assertIsNotNone(err)


class ManualAuditGuardTests(unittest.TestCase):
    def test_non_manual_passes(self) -> None:
        self.assertIsNone(validate_manual_audit_guard("quick_scan"))

    def test_manual_without_flag_blocked(self) -> None:
        err = validate_manual_audit_guard("manual_audit_assisted")
        self.assertIsNotNone(err)
        self.assertIn("manual_review", err)

    def test_manual_with_flag_passes(self) -> None:
        self.assertIsNone(
            validate_manual_audit_guard("manual_audit_assisted", manual_review_flag=True)
        )

    def test_manual_with_authorization_passes(self) -> None:
        self.assertIsNone(
            validate_manual_audit_guard("manual_audit_assisted", authorization_placeholder=True)
        )


class RetestCategoryTests(unittest.TestCase):
    def test_non_retest_passes(self) -> None:
        self.assertIsNone(validate_retest_categories("quick_scan", []))

    def test_retest_no_categories_fails(self) -> None:
        err = validate_retest_categories("retest_scan", [])
        self.assertIsNotNone(err)
        self.assertIn("at least one", err)

    def test_retest_one_category_passes(self) -> None:
        self.assertIsNone(validate_retest_categories("retest_scan", ["prompt_injection"]))

    def test_retest_three_categories_passes(self) -> None:
        self.assertIsNone(
            validate_retest_categories("retest_scan", ["prompt_injection", "cost_abuse", "rag_data_leakage"])
        )

    def test_retest_four_categories_blocked(self) -> None:
        err = validate_retest_categories("retest_scan", [
            "prompt_injection", "cost_abuse", "rag_data_leakage", "tool_function_abuse",
        ])
        self.assertIsNotNone(err)
        self.assertIn("at most 3", err)


class PayloadSecretTests(unittest.TestCase):
    def test_clean_payload(self) -> None:
        self.assertIsNone(validate_payload_no_secrets({"name": "test", "type": "mock"}))

    def test_secret_field_detected(self) -> None:
        err = validate_payload_no_secrets({"api_key": "sk-12345"})
        self.assertIsNotNone(err)
        self.assertIn("secret", err)

    def test_nested_secret_detected(self) -> None:
        err = validate_payload_no_secrets({"target": {"bearer_token": "abc"}})
        self.assertIsNotNone(err)

    def test_multiple_secrets_detected(self) -> None:
        err = validate_payload_no_secrets({"api_key": "x", "password": "y"})
        self.assertIsNotNone(err)


class CompositeScanValidationTests(unittest.TestCase):
    def test_valid_quick_scan(self) -> None:
        result = validate_scan_request(
            "quick_scan",
            verification_status="verified",
            requested_categories=["prompt_injection"],
            requested_max_tests=5,
            requested_timeout=60,
            requested_concurrency=1,
        )
        self.assertTrue(result.valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(result.resolved_scan_type, "quick_scan")
        self.assertIsNotNone(result.resolved_config)

    def test_unknown_scan_type_fails_fast(self) -> None:
        result = validate_scan_request("nonexistent", verification_status="verified")
        self.assertFalse(result.valid)
        self.assertEqual(len(result.errors), 1)

    def test_multiple_errors_collected(self) -> None:
        result = validate_scan_request(
            "quick_scan",
            verification_status="unverified",
            requested_categories=["rag_data_leakage"],
            requested_max_tests=999,
        )
        self.assertFalse(result.valid)
        self.assertTrue(len(result.errors) >= 2)

    def test_disabled_scan_type_error(self) -> None:
        result = validate_scan_request(
            "deep_scan",
            verification_status="verified",
            requested_max_tests=10,
        )
        self.assertFalse(result.valid)
        self.assertTrue(any("disabled" in e for e in result.errors))

    def test_manual_audit_without_flags(self) -> None:
        result = validate_scan_request(
            "manual_audit_assisted",
            verification_status="verified",
        )
        self.assertFalse(result.valid)
        self.assertTrue(any("manual_review" in e for e in result.errors))

    def test_manual_audit_with_flags(self) -> None:
        result = validate_scan_request(
            "manual_audit_assisted",
            verification_status="verified",
            manual_review_flag=True,
        )
        # Still has disabled error but no manual guard error
        manual_guard_errors = [e for e in result.errors if "manual_review flag" in e]
        self.assertEqual(len(manual_guard_errors), 0)

    def test_retest_broad_categories(self) -> None:
        result = validate_scan_request(
            "retest_scan",
            verification_status="verified",
            requested_categories=["prompt_injection", "cost_abuse", "rag_data_leakage", "tool_function_abuse"],
        )
        self.assertFalse(result.valid)
        self.assertTrue(any("at most 3" in e for e in result.errors))

    def test_payload_secrets_rejected(self) -> None:
        result = validate_scan_request(
            "quick_scan",
            verification_status="verified",
            payload={"api_key": "sk-12345"},
        )
        self.assertFalse(result.valid)
        self.assertTrue(any("secret" in e for e in result.errors))

    def test_serialization(self) -> None:
        result = validate_scan_request("quick_scan", verification_status="verified")
        data = result.to_dict()
        self.assertIn("valid", data)
        self.assertIn("errors", data)
        self.assertIn("resolved_scan_type", data)


if __name__ == "__main__":
    unittest.main()
