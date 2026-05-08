from __future__ import annotations

from pydantic import BaseModel, Field

from .common import ModuleStatus


class TargetsModuleStatus(ModuleStatus):
    module: str = "targets"
    status: str = "setup_contract_placeholder"
    purpose: str = "Future target setup metadata contract before ownership verification and scanning."
    future_phase: str = "Phase 14 ownership verification"


class TargetSetupContract(BaseModel):
    purpose: str = "Phase 13 future request contract for safe target metadata."
    current_behavior: str = "No route persists targets, verifies ownership, stores secrets, or starts scans."
    safe_fields: list[str] = Field(
        default_factory=lambda: [
            "target_name",
            "target_type",
            "url",
            "http_method",
            "auth_type",
            "request_response_notes",
            "rate_limit_notes",
            "test_account_notes",
            "rag_private_docs_involved",
            "tools_actions_involved",
            "production_impact_acknowledgement",
            "authorization_scope_acknowledgement",
        ]
    )
    ui_target_types: list[str] = Field(
        default_factory=lambda: [
            "api_endpoint",
            "openai_compatible_endpoint",
            "vercel_ai_sdk_endpoint",
            "rag_application",
            "tool_using_agent",
            "chatbot_url",
            "manual_audit_target",
        ]
    )
    database_target_type_notes: str = (
        "The Phase 10 database enum currently supports api_endpoint, openai_compatible, "
        "vercel_ai_sdk, langchain, llamaindex, chatbot_url, and manual. Reconcile generic "
        "Phase 13 UI labels with a reviewed migration before enabling persistence."
    )
    allowed_http_methods: list[str] = Field(default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE"])
    allowed_auth_types: list[str] = Field(
        default_factory=lambda: ["none", "bearer_token_placeholder", "api_key_placeholder", "test_account_manual"]
    )
    forbidden_fields: list[str] = Field(
        default_factory=lambda: [
            "plaintext_api_key",
            "plaintext_bearer_token",
            "password",
            "cookies",
            "private_key",
            "raw_headers",
            "production_credentials",
        ]
    )
