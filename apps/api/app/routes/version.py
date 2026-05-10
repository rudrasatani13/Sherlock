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
            status="setup_contract_placeholder",
            purpose="Phase 13 project setup metadata contract and static dashboard UI foundation.",
            future_phase="Future authenticated persistence after reviewed auth, tenant, and database integration",
            available_endpoints=[f"GET {api_prefix}/projects"],
            future_capabilities=["project setup metadata", "team ownership", "dashboard project selection"],
            disabled_capabilities=[
                "active API persistence",
                "project authorization",
                "database writes from dashboard UI",
                "real production project persistence",
            ],
        ),
        ModuleStatus(
            module="targets",
            status="setup_contract_placeholder",
            purpose="Phase 13 target setup metadata contract before verification and scanning.",
            future_phase="Phase 14 ownership verification",
            available_endpoints=[f"GET {api_prefix}/targets"],
            future_capabilities=["safe target metadata", "ownership state", "approved scope boundaries"],
            disabled_capabilities=[
                "target verification",
                "active API persistence",
                "secret storage",
                "public scanning",
                "scanner execution",
                "SSRF protection implementation",
            ],
        ),
        ModuleStatus(
            module="scans",
            status="scan_types_and_limits_foundation",
            purpose="Phase 16 scan types, limits, plan tiers, and category matrix foundation. Builds on Phase 15 queue/worker with bounded scan modes.",
            future_phase="Future production scan execution after auth, verification, SSRF protection, rate limits, and billing",
            available_endpoints=[
                f"GET {api_prefix}/scans",
                f"GET {api_prefix}/scans/types",
                f"GET {api_prefix}/scans/limits",
            ],
            future_capabilities=[
                "scan job creation (authenticated + verified)",
                "scan job status queries",
                "scan job cancellation",
                "queue worker handoff",
                "worker result ingestion",
                "scan type selection and limit enforcement",
            ],
            disabled_capabilities=[
                "public scan creation",
                "production queue deployment",
                "scanner execution from API routes",
                "real network scanning",
                "active scan persistence",
                "billing enforcement",
            ],
        ),
        ModuleStatus(
            module="findings",
            status="findings_system_foundation",
            purpose="Phase 17 structured findings contract and static schema metadata.",
            future_phase="Future production findings retrieval after auth, persistence, and access controls",
            available_endpoints=[f"GET {api_prefix}/findings", f"GET {api_prefix}/findings/schema"],
            future_capabilities=[
                "finding record retrieval after auth and persistence exist",
                "manual review workflows",
                "retest state integration",
                "production web report consumption",
            ],
            disabled_capabilities=[
                "active finding persistence",
                "automatic customer-facing findings",
                "database reads or writes",
                "report generation",
                "PDF export",
            ],
        ),
        ModuleStatus(
            module="reports",
            status="pdf_export_foundation",
            purpose="Phase 18 web report schema metadata plus Phase 19 PDF export contract and local/demo print-ready HTML foundation.",
            future_phase="Future production report access, secure storage, paid gates, and customer PDF delivery",
            available_endpoints=[f"GET {api_prefix}/reports", f"GET {api_prefix}/reports/schema"],
            future_capabilities=["authenticated report access", "report persistence", "report sharing controls", "production PDF delivery"],
            disabled_capabilities=[
                "active report persistence",
                "real customer report retrieval",
                "public PDF download links",
                "billing gates",
                "public report sharing links",
            ],
        ),
        ModuleStatus(
            module="verification",
            status="contract_placeholder",
            purpose="Phase 14 target ownership verification contracts, method definitions, and challenge token design.",
            future_phase="Phase 15 scan execution after verification",
            available_endpoints=[f"GET {api_prefix}/verification"],
            future_capabilities=[
                "DNS TXT verification",
                "HTML meta tag verification",
                "well-known file verification",
                "manual authorization review",
                "chatbot/API challenge verification",
                "challenge token generation",
                "verification status tracking",
            ],
            disabled_capabilities=[
                "production DNS/HTTP/chatbot verification checks",
                "active API persistence",
                "SSRF-safe network requests",
                "public scan unlocks",
            ],
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
                "queue_backend": settings.queue_backend,
                "public_scanning_enabled": settings.public_scanning_enabled,
            },
        },
        error=None,
        metadata=build_metadata(),
    )
