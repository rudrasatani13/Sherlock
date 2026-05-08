from __future__ import annotations

from pydantic import BaseModel, Field

from .common import ModuleStatus


class ProjectsModuleStatus(ModuleStatus):
    module: str = "projects"
    status: str = "setup_contract_placeholder"
    purpose: str = "Future project setup metadata contract for authenticated Sherlock workspaces."
    future_phase: str = "Future authenticated persistence after Phase 13 UI contract"


class ProjectSetupContract(BaseModel):
    purpose: str = "Phase 13 future request contract for project setup metadata."
    current_behavior: str = "No route persists project records; dashboard setup UI remains static/mock."
    safe_fields: list[str] = Field(
        default_factory=lambda: [
            "project_name",
            "description",
            "environment",
            "app_type",
            "data_sensitivity",
            "framework_or_stack",
            "notes",
        ]
    )
    allowed_environments: list[str] = Field(default_factory=lambda: ["staging", "production", "development"])
    allowed_app_types: list[str] = Field(
        default_factory=lambda: ["chatbot", "rag_app", "agent", "support_bot", "internal_assistant", "other"]
    )
    allowed_data_sensitivity: list[str] = Field(
        default_factory=lambda: ["public", "internal", "customer_data", "regulated_sensitive"]
    )
    forbidden_fields: list[str] = Field(
        default_factory=lambda: [
            "api_keys",
            "bearer_tokens",
            "passwords",
            "cookies",
            "private_keys",
            "raw_auth_headers",
        ]
    )
