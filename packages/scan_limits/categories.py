"""Sherlock vulnerability category registry and scan-type category mapping.

Maps scan types to allowed prompt-library categories from Phase 6.
The category IDs match the manifest.json entries in packages/prompt_library.
"""
from __future__ import annotations

from typing import Dict, FrozenSet, List


# ---------------------------------------------------------------------------
# All categories from Phase 6 prompt library manifest
# ---------------------------------------------------------------------------

ALL_CATEGORIES: FrozenSet[str] = frozenset({
    "prompt_injection",
    "system_prompt_leakage",
    "sensitive_data_leakage",
    "rag_data_leakage",
    "indirect_prompt_injection",
    "tool_function_abuse",
    "unsafe_output_handling",
    "cost_abuse",
})

CATEGORY_DISPLAY_NAMES: Dict[str, str] = {
    "prompt_injection": "Prompt Injection",
    "system_prompt_leakage": "System Prompt Leakage",
    "sensitive_data_leakage": "Sensitive Data Leakage",
    "rag_data_leakage": "RAG Data Leakage / Document Exfiltration",
    "indirect_prompt_injection": "Indirect Prompt Injection",
    "tool_function_abuse": "Tool / Function Abuse",
    "unsafe_output_handling": "Unsafe Output Handling",
    "cost_abuse": "Cost Abuse / Unbounded Consumption",
}


# ---------------------------------------------------------------------------
# Core category subsets
# ---------------------------------------------------------------------------

CORE_CATEGORIES: FrozenSet[str] = frozenset({
    "prompt_injection",
    "system_prompt_leakage",
    "sensitive_data_leakage",
    "unsafe_output_handling",
})

STANDARD_CATEGORIES: FrozenSet[str] = frozenset({
    "prompt_injection",
    "system_prompt_leakage",
    "sensitive_data_leakage",
    "rag_data_leakage",
    "unsafe_output_handling",
    "cost_abuse",
})

DEEP_CATEGORIES: FrozenSet[str] = ALL_CATEGORIES

QUICK_CATEGORIES: FrozenSet[str] = frozenset({
    "prompt_injection",
    "system_prompt_leakage",
    "unsafe_output_handling",
})

# Categories requiring special capability flags
RAG_CATEGORIES: FrozenSet[str] = frozenset({"rag_data_leakage"})
TOOL_CATEGORIES: FrozenSet[str] = frozenset({"tool_function_abuse"})
INDIRECT_INJECTION_CATEGORIES: FrozenSet[str] = frozenset({"indirect_prompt_injection"})
COST_ABUSE_CATEGORIES: FrozenSet[str] = frozenset({"cost_abuse"})


# ---------------------------------------------------------------------------
# Per-scan-type category mapping
# ---------------------------------------------------------------------------

SCAN_TYPE_CATEGORIES: Dict[str, FrozenSet[str]] = {
    "quick_scan": QUICK_CATEGORIES,
    "standard_scan": STANDARD_CATEGORIES,
    "deep_scan": DEEP_CATEGORIES,
    "manual_audit_assisted": DEEP_CATEGORIES,
    "retest_scan": ALL_CATEGORIES,  # targeted_categories_only enforced by validator
}


def get_categories_for_scan_type(scan_type: str) -> List[str]:
    """Return sorted list of category IDs allowed for a scan type."""
    categories = SCAN_TYPE_CATEGORIES.get(scan_type, frozenset())
    return sorted(categories)


def is_category_valid(category: str) -> bool:
    """Return True if category is a recognized Sherlock vulnerability category."""
    return category in ALL_CATEGORIES
