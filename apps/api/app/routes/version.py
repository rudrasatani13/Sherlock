from __future__ import annotations

from fastapi import APIRouter

from ..config import get_settings
from ..errors import build_metadata
from ..schemas.common import ApiResponse, ModuleStatus, serialize_model

router = APIRouter(tags=["version"])


def _module_statuses(api_prefix: str) -> list[ModuleStatus]:
    return [
        ModuleStatus(
            module="health",
            status="available",
            purpose="Confirms the API process is running.",
            available_endpoints=["GET /health"],
        ),
        ModuleStatus(
            module="version",
            status="available",
            purpose="Describes current phase status and future route groups.",
            available_endpoints=["GET /version"],
        ),
        ModuleStatus(
            module="auth",
            status="foundation_only",
            purpose="Supabase Auth-compatible configuration status and protected current-user route foundation.",
            future_phase="Future production token validation and dashboard session integration",
            available_endpoints=[f"GET {api_prefix}/auth/status", f"GET {api_prefix}/me"],
            future_capabilities=["Supabase JWT validation", "current user profile loading", "organization membership authorization"],
            disabled_capabilities=["login/signup endpoints", "dashboard sessions", "database writes from auth flows"],
        ),
        ModuleStatus(
            module="projects",
            status="placeholder_only",
            purpose="Future project/workspace organization.",
            future_phase="Phase 13 project setup and persistence integration",
            available_endpoints=[f"GET {api_prefix}/projects"],
            future_capabilities=["project records", "team ownership", "dashboard project selection"],
            disabled_capabilities=["active API persistence", "project authorization", "authenticated dashboard API integration"],
        ),
        ModuleStatus(
            module="targets",
            status="placeholder_only",
            purpose="Future target records and verification state.",
            future_phase="Phase 14 ownership verification",
            available_endpoints=[f"GET {api_prefix}/targets"],
            future_capabilities=["target metadata", "ownership state", "approved scope boundaries"],
            disabled_capabilities=["target verification", "active API persistence", "public scanning", "SSRF protection implementation"],
        ),
        ModuleStatus(
            module="scans",
            status="placeholder_only",
            purpose="Future scan request and worker handoff contracts.",
            future_phase="Phase 15 queue workers after required security controls",
            available_endpoints=[f"GET {api_prefix}/scans"],
            future_capabilities=["scan jobs", "scan status", "worker integration"],
            disabled_capabilities=["scanner execution", "queue workers", "active API persistence", "public scan creation"],
        ),
        ModuleStatus(
            module="findings",
            status="placeholder_only",
            purpose="Future reviewed findings system.",
            future_phase="Phase 17 findings system",
            available_endpoints=[f"GET {api_prefix}/findings"],
            future_capabilities=["finding records", "severity", "confidence", "status", "manual review"],
            disabled_capabilities=["active finding persistence", "automatic customer-facing findings"],
        ),
        ModuleStatus(
            module="reports",
            status="placeholder_only",
            purpose="Future report metadata and web report access contracts.",
            future_phase="Phase 18 web report",
            available_endpoints=[f"GET {api_prefix}/reports"],
            future_capabilities=["web report metadata", "report access", "report status"],
            disabled_capabilities=["active report persistence", "real report generation", "PDF export"],
        ),
        ModuleStatus(
            module="verification",
            status="placeholder_only",
            purpose="Future target ownership verification before any public scanning.",
            future_phase="Phase 14 ownership verification",
            available_endpoints=[f"GET {api_prefix}/verification"],
            future_capabilities=["ownership verification records", "verification status"],
            disabled_capabilities=["production target verification logic", "active API persistence", "public scan unlocks"],
        ),
    ]


@router.get("/version", response_model=ApiResponse)
def version_status() -> ApiResponse:
    settings = get_settings()
    return ApiResponse(
        success=True,
        data={
            "product_name": settings.app_name,
            "brand_name": settings.brand_name,
            "marketing_name": settings.marketing_name,
            "api_version": settings.api_version,
            "current_phase": settings.current_phase,
            "modules": [serialize_model(module) for module in _module_statuses(settings.api_prefix)],
            "security_boundaries": {
                "database_enabled": settings.database_enabled,
                "authentication_enabled": settings.authentication_enabled,
                "auth_provider": "supabase",
                "auth_token_validation_active": False,
                "billing_enabled": settings.billing_enabled,
                "worker_enabled": settings.worker_enabled,
                "public_scanning_enabled": settings.public_scanning_enabled,
            },
        },
        error=None,
        metadata=build_metadata(),
    )
