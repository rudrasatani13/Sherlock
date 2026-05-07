from __future__ import annotations

from fastapi import Header

from .config import Settings, get_settings
from .errors import AppError
from .schemas.auth import AuthConfigurationStatus, CurrentUser
from .schemas.common import serialize_model


class AuthUnavailableError(AppError):
    def __init__(self, details: object | None = None) -> None:
        super().__init__(
            status_code=503,
            code="auth_unavailable",
            message="Authentication is not available in this Sherlock environment yet.",
            details=details,
        )


class AuthenticationRequiredError(AppError):
    def __init__(self, details: object | None = None) -> None:
        super().__init__(
            status_code=401,
            code="authentication_required",
            message="A valid Supabase Auth bearer token is required for this route.",
            details=details,
        )


def build_auth_configuration_status(settings: Settings | None = None) -> AuthConfigurationStatus:
    active_settings = settings or get_settings()
    return AuthConfigurationStatus(
        authentication_enabled=active_settings.authentication_enabled,
        supabase_project_configured=active_settings.supabase_project_configured,
        supabase_url_configured=active_settings.supabase_url_configured,
        supabase_anon_key_configured=active_settings.supabase_anon_key_configured,
        service_role_key_configured_server_side=active_settings.supabase_service_role_key_configured,
        jwt_verification_configured=active_settings.supabase_jwks_url_configured,
        token_validation_active=False,
        production_ready=False,
        local_development_mode=not active_settings.authentication_enabled,
        public_endpoints=["/health", "/version", f"{active_settings.api_prefix}/auth/status"],
        protected_endpoints=[f"{active_settings.api_prefix}/me"],
        disabled_capabilities=[
            "login/signup endpoints",
            "production JWT verification",
            "dashboard sessions",
            "database writes from auth flows",
            "service-role usage in browser code",
        ],
    )


def extract_bearer_token(authorization: str | None) -> str:
    if authorization is None:
        raise AuthenticationRequiredError({"reason": "missing_authorization_header"})
    scheme, separator, token = authorization.partition(" ")
    if separator == "" or scheme.lower() != "bearer" or token.strip() == "":
        raise AuthenticationRequiredError({"reason": "invalid_authorization_header"})
    return token.strip()


def require_current_user(authorization: str | None = Header(default=None, alias="Authorization")) -> CurrentUser:
    settings = get_settings()
    status = build_auth_configuration_status(settings)
    if not settings.authentication_enabled:
        raise AuthUnavailableError(
            {
                "reason": "auth_disabled",
                "status": serialize_model(status),
            }
        )
    if not settings.supabase_project_configured or not settings.supabase_jwks_url_configured:
        raise AuthUnavailableError(
            {
                "reason": "supabase_auth_not_configured",
                "required": ["SUPABASE_URL", "SUPABASE_ANON_KEY", "SUPABASE_JWKS_URL"],
                "status": serialize_model(status),
            }
        )
    extract_bearer_token(authorization)
    raise AuthUnavailableError(
        {
            "reason": "jwt_verification_not_active",
            "status": serialize_model(status),
        }
    )
