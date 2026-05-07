from __future__ import annotations

from fastapi import APIRouter

from ..config import get_settings
from ..errors import build_metadata
from ..schemas.common import ApiResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse)
def health_check() -> ApiResponse:
    settings = get_settings()
    return ApiResponse(
        success=True,
        data={
            "app_name": settings.app_name,
            "brand_name": settings.brand_name,
            "marketing_name": settings.marketing_name,
            "status": "ok",
            "version": settings.api_version,
            "environment": settings.environment,
            "public_scanning_enabled": settings.public_scanning_enabled,
        },
        error=None,
        metadata=build_metadata(),
    )
