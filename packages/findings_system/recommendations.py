"""Fix recommendation templates for Phase 17 findings."""
from __future__ import annotations

from .categories import normalize_category


RECOMMENDATION_TEMPLATES: dict[str, str] = {
    "prompt_injection": (
        "Separate trusted instructions from user-controlled content, enforce policy and authorization checks outside "
        "the model, label untrusted context clearly, and add regression tests for the bypass pattern."
    ),
    "system_prompt_leakage": (
        "Remove secrets and sensitive operational details from system prompts, minimize hidden instruction content, "
        "and enforce data and tool permissions outside prompt text."
    ),
    "sensitive_data_leakage": (
        "Enforce tenant and role access checks before retrieval or tool calls, redact sensitive values before model "
        "responses, and add isolation tests for the affected data path."
    ),
    "rag_data_leakage": (
        "Add document-level authorization, retrieval filters, source attribution, and access checks before retrieved "
        "content is sent to the model."
    ),
    "indirect_prompt_injection": (
        "Treat retrieved or web content as untrusted, sanitize and isolate it from instructions, and require explicit "
        "confirmation before tool use influenced by external content."
    ),
    "tool_function_abuse": (
        "Add tool allowlists, server-side permission checks, argument validation, and human confirmation for risky or "
        "state-changing actions."
    ),
    "unsafe_output_handling": (
        "Render model output through safe sanitization, escape HTML and script-capable content by default, and enforce "
        "output policies before displaying or forwarding responses."
    ),
    "cost_abuse_unbounded_consumption": (
        "Add rate limits, token budgets, timeout and cancellation controls, retry caps, and monitoring for unusually "
        "large or repeated model output."
    ),
    "other_unknown": (
        "Review the observed behavior manually, confirm the affected control and impact, then add a category-specific "
        "fix plan before treating this as customer-facing."
    ),
}


def recommendation_for_category(category: str, fallback: str = "") -> str:
    """Return a plain-English fix recommendation for *category*."""
    normalized = normalize_category(category)
    recommendation = RECOMMENDATION_TEMPLATES.get(normalized)
    if recommendation:
        return recommendation
    return fallback or RECOMMENDATION_TEMPLATES["other_unknown"]
