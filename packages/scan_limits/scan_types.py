"""Scan type definitions and limit configuration for Sherlock.

Each scan type defines bounded limits for test count, timeout, concurrency,
response size, category inclusion, verification requirements, and report level.

All limits are configurable through this module. Future phases may load
overrides from environment or database; the current V0 uses static defaults.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional

from .categories import (
    ALL_CATEGORIES,
    DEEP_CATEGORIES,
    QUICK_CATEGORIES,
    STANDARD_CATEGORIES,
)


# ---------------------------------------------------------------------------
# Scan type enum-like constants
# ---------------------------------------------------------------------------

class ScanType:
    QUICK_SCAN = "quick_scan"
    STANDARD_SCAN = "standard_scan"
    DEEP_SCAN = "deep_scan"
    MANUAL_AUDIT_ASSISTED = "manual_audit_assisted"
    RETEST_SCAN = "retest_scan"

    ALL: FrozenSet[str] = frozenset({
        "quick_scan",
        "standard_scan",
        "deep_scan",
        "manual_audit_assisted",
        "retest_scan",
    })


# ---------------------------------------------------------------------------
# Report level constants
# ---------------------------------------------------------------------------

class ReportLevel:
    SUMMARY = "summary"
    STANDARD = "standard"
    DETAILED = "detailed"
    MANUAL_REVIEW = "manual_review"
    RETEST = "retest"


# ---------------------------------------------------------------------------
# Scan type configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ScanTypeConfig:
    """Immutable scan type definition with limits and rules."""
    scan_type: str
    display_name: str
    description: str
    max_tests: int
    timeout_seconds: int
    max_concurrency: int
    max_response_chars_per_test: int
    max_prompt_chars_per_test: int
    included_categories: FrozenSet[str]
    excluded_categories: FrozenSet[str]
    requires_verified_target: bool
    requires_manual_review: bool
    allow_rag_tests: bool
    allow_tool_tests: bool
    allow_indirect_injection_tests: bool
    allow_cost_abuse_tests: bool
    report_level: str
    queue_priority: int
    enabled: bool
    future_plan_availability: List[str] = field(default_factory=list)
    targeted_categories_only: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scan_type": self.scan_type,
            "display_name": self.display_name,
            "description": self.description,
            "max_tests": self.max_tests,
            "timeout_seconds": self.timeout_seconds,
            "max_concurrency": self.max_concurrency,
            "max_response_chars_per_test": self.max_response_chars_per_test,
            "max_prompt_chars_per_test": self.max_prompt_chars_per_test,
            "included_categories": sorted(self.included_categories),
            "excluded_categories": sorted(self.excluded_categories),
            "requires_verified_target": self.requires_verified_target,
            "requires_manual_review": self.requires_manual_review,
            "allow_rag_tests": self.allow_rag_tests,
            "allow_tool_tests": self.allow_tool_tests,
            "allow_indirect_injection_tests": self.allow_indirect_injection_tests,
            "allow_cost_abuse_tests": self.allow_cost_abuse_tests,
            "report_level": self.report_level,
            "queue_priority": self.queue_priority,
            "enabled": self.enabled,
            "future_plan_availability": list(self.future_plan_availability),
            "targeted_categories_only": self.targeted_categories_only,
        }


# ---------------------------------------------------------------------------
# V0 scan type definitions
# ---------------------------------------------------------------------------

SCAN_TYPES: Dict[str, ScanTypeConfig] = {
    ScanType.QUICK_SCAN: ScanTypeConfig(
        scan_type=ScanType.QUICK_SCAN,
        display_name="Quick Scan",
        description="A small preflight check with limited categories. Low cost, fast turnaround. Useful for early demos and free-tier usage later.",
        max_tests=10,
        timeout_seconds=120,
        max_concurrency=1,
        max_response_chars_per_test=4000,
        max_prompt_chars_per_test=2000,
        included_categories=QUICK_CATEGORIES,
        excluded_categories=ALL_CATEGORIES - QUICK_CATEGORIES,
        requires_verified_target=True,
        requires_manual_review=False,
        allow_rag_tests=False,
        allow_tool_tests=False,
        allow_indirect_injection_tests=False,
        allow_cost_abuse_tests=False,
        report_level=ReportLevel.SUMMARY,
        queue_priority=3,
        enabled=True,
        future_plan_availability=["free", "launch_scan", "builder", "startup", "manual_audit"],
    ),
    ScanType.STANDARD_SCAN: ScanTypeConfig(
        scan_type=ScanType.STANDARD_SCAN,
        display_name="Standard Scan",
        description="A balanced launch-readiness scan covering core vulnerability categories. Moderate test count and timeout. Future web report eligible.",
        max_tests=50,
        timeout_seconds=600,
        max_concurrency=2,
        max_response_chars_per_test=8000,
        max_prompt_chars_per_test=4000,
        included_categories=STANDARD_CATEGORIES,
        excluded_categories=ALL_CATEGORIES - STANDARD_CATEGORIES,
        requires_verified_target=True,
        requires_manual_review=False,
        allow_rag_tests=True,
        allow_tool_tests=False,
        allow_indirect_injection_tests=False,
        allow_cost_abuse_tests=True,
        report_level=ReportLevel.STANDARD,
        queue_priority=2,
        enabled=True,
        future_plan_availability=["launch_scan", "builder", "startup", "manual_audit"],
    ),
    ScanType.DEEP_SCAN: ScanTypeConfig(
        scan_type=ScanType.DEEP_SCAN,
        display_name="Deep Scan",
        description="A thorough review for serious AI applications. Covers all vulnerability categories including RAG, tool abuse, and indirect injection. Stricter queue limits.",
        max_tests=150,
        timeout_seconds=1800,
        max_concurrency=3,
        max_response_chars_per_test=12000,
        max_prompt_chars_per_test=6000,
        included_categories=DEEP_CATEGORIES,
        excluded_categories=frozenset(),
        requires_verified_target=True,
        requires_manual_review=False,
        allow_rag_tests=True,
        allow_tool_tests=True,
        allow_indirect_injection_tests=True,
        allow_cost_abuse_tests=True,
        report_level=ReportLevel.DETAILED,
        queue_priority=1,
        enabled=False,  # Disabled until paid plan gates exist
        future_plan_availability=["builder", "startup", "manual_audit"],
    ),
    ScanType.MANUAL_AUDIT_ASSISTED: ScanTypeConfig(
        scan_type=ScanType.MANUAL_AUDIT_ASSISTED,
        display_name="Manual Audit Assisted",
        description="Semi-automated support for Phase 8 manual audit workflow. Not available as public self-serve. Requires manual review and auditor-controlled scope.",
        max_tests=250,
        timeout_seconds=3600,
        max_concurrency=2,
        max_response_chars_per_test=12000,
        max_prompt_chars_per_test=6000,
        included_categories=DEEP_CATEGORIES,
        excluded_categories=frozenset(),
        requires_verified_target=True,
        requires_manual_review=True,
        allow_rag_tests=True,
        allow_tool_tests=True,
        allow_indirect_injection_tests=True,
        allow_cost_abuse_tests=True,
        report_level=ReportLevel.MANUAL_REVIEW,
        queue_priority=1,
        enabled=False,  # Not self-serve
        future_plan_availability=["manual_audit"],
    ),
    ScanType.RETEST_SCAN: ScanTypeConfig(
        scan_type=ScanType.RETEST_SCAN,
        display_name="Retest Scan",
        description="A focused retest for a specific finding or category after fixes. Small targeted test set, cheaper and faster. Tied to a previous scan or finding later.",
        max_tests=20,
        timeout_seconds=300,
        max_concurrency=1,
        max_response_chars_per_test=4000,
        max_prompt_chars_per_test=2000,
        included_categories=ALL_CATEGORIES,  # Restricted by targeted_categories_only
        excluded_categories=frozenset(),
        requires_verified_target=True,
        requires_manual_review=False,
        allow_rag_tests=True,
        allow_tool_tests=True,
        allow_indirect_injection_tests=True,
        allow_cost_abuse_tests=True,
        report_level=ReportLevel.RETEST,
        queue_priority=2,
        enabled=True,
        future_plan_availability=["launch_scan", "builder", "startup", "manual_audit"],
        targeted_categories_only=True,
    ),
}


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def get_scan_type(name: str) -> Optional[ScanTypeConfig]:
    """Return the ScanTypeConfig for a given scan type name, or None."""
    return SCAN_TYPES.get(name)


def get_scan_type_names() -> List[str]:
    """Return sorted list of all defined scan type names."""
    return sorted(SCAN_TYPES.keys())


def is_scan_type_enabled(name: str) -> bool:
    """Return True if the scan type exists and is currently enabled."""
    config = SCAN_TYPES.get(name)
    return config is not None and config.enabled
