"""Category normalization for Phase 17 findings."""
from __future__ import annotations


CATEGORY_PROMPT_INJECTION = "prompt_injection"
CATEGORY_SYSTEM_PROMPT_LEAKAGE = "system_prompt_leakage"
CATEGORY_SENSITIVE_DATA_LEAKAGE = "sensitive_data_leakage"
CATEGORY_RAG_DATA_LEAKAGE = "rag_data_leakage"
CATEGORY_INDIRECT_PROMPT_INJECTION = "indirect_prompt_injection"
CATEGORY_TOOL_FUNCTION_ABUSE = "tool_function_abuse"
CATEGORY_UNSAFE_OUTPUT_HANDLING = "unsafe_output_handling"
CATEGORY_COST_ABUSE = "cost_abuse_unbounded_consumption"
CATEGORY_OTHER_UNKNOWN = "other_unknown"

KNOWN_CATEGORIES: tuple[str, ...] = (
    CATEGORY_PROMPT_INJECTION,
    CATEGORY_SYSTEM_PROMPT_LEAKAGE,
    CATEGORY_SENSITIVE_DATA_LEAKAGE,
    CATEGORY_RAG_DATA_LEAKAGE,
    CATEGORY_INDIRECT_PROMPT_INJECTION,
    CATEGORY_TOOL_FUNCTION_ABUSE,
    CATEGORY_UNSAFE_OUTPUT_HANDLING,
    CATEGORY_COST_ABUSE,
    CATEGORY_OTHER_UNKNOWN,
)

CATEGORY_DISPLAY_NAMES: dict[str, str] = {
    CATEGORY_PROMPT_INJECTION: "Prompt injection",
    CATEGORY_SYSTEM_PROMPT_LEAKAGE: "System prompt leakage",
    CATEGORY_SENSITIVE_DATA_LEAKAGE: "Sensitive data leakage",
    CATEGORY_RAG_DATA_LEAKAGE: "RAG data leakage",
    CATEGORY_INDIRECT_PROMPT_INJECTION: "Indirect prompt injection",
    CATEGORY_TOOL_FUNCTION_ABUSE: "Tool/function abuse",
    CATEGORY_UNSAFE_OUTPUT_HANDLING: "Unsafe output handling",
    CATEGORY_COST_ABUSE: "Cost abuse / unbounded consumption",
    CATEGORY_OTHER_UNKNOWN: "Other / unknown",
}

CATEGORY_ALIASES: dict[str, str] = {
    "canary_token_leakage": CATEGORY_RAG_DATA_LEAKAGE,
    "cost_abuse": CATEGORY_COST_ABUSE,
    "cost_abuse_unbounded": CATEGORY_COST_ABUSE,
    "cost_abuse_or_unbounded_consumption": CATEGORY_COST_ABUSE,
    "data_leakage": CATEGORY_SENSITIVE_DATA_LEAKAGE,
    "sensitive_data_pattern": CATEGORY_SENSITIVE_DATA_LEAKAGE,
    "system_prompt": CATEGORY_SYSTEM_PROMPT_LEAKAGE,
    "tool_abuse": CATEGORY_TOOL_FUNCTION_ABUSE,
    "unsafe_output": CATEGORY_UNSAFE_OUTPUT_HANDLING,
    "unknown": CATEGORY_OTHER_UNKNOWN,
    "safe_smoke": CATEGORY_OTHER_UNKNOWN,
}


def normalize_category(value: str | None) -> str:
    """Map existing Sherlock category names and evaluator groups to Phase 17 categories."""
    normalized = (value or "").strip().lower().replace(" ", "_").replace("-", "_")
    normalized = CATEGORY_ALIASES.get(normalized, normalized)
    if normalized in KNOWN_CATEGORIES:
        return normalized
    return CATEGORY_OTHER_UNKNOWN


def category_display_name(value: str | None) -> str:
    return CATEGORY_DISPLAY_NAMES[normalize_category(value)]


def is_known_category(value: str | None) -> bool:
    return normalize_category(value) != CATEGORY_OTHER_UNKNOWN
