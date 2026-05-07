from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class OrganizationMembership(BaseModel):
    organization_id: str
    role: str
    organization_name: Optional[str] = None


class CurrentUserProfile(BaseModel):
    id: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    onboarding_status: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CurrentUser(BaseModel):
    id: str
    email: Optional[str] = None
    auth_provider: str = "supabase"
    profile: Optional[CurrentUserProfile] = None
    memberships: List[OrganizationMembership] = Field(default_factory=list)


class AuthConfigurationStatus(BaseModel):
    provider: str = "supabase"
    authentication_enabled: bool
    supabase_project_configured: bool
    supabase_url_configured: bool
    supabase_anon_key_configured: bool
    service_role_key_configured_server_side: bool
    jwt_verification_configured: bool
    token_validation_active: bool
    production_ready: bool
    local_development_mode: bool
    public_endpoints: List[str] = Field(default_factory=list)
    protected_endpoints: List[str] = Field(default_factory=list)
    disabled_capabilities: List[str] = Field(default_factory=list)
