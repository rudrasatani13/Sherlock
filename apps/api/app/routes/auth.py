from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth import build_auth_configuration_status, require_current_user
from ..errors import build_metadata
from ..schemas.auth import CurrentUser
from ..schemas.common import ApiResponse, serialize_model

router = APIRouter(tags=["auth"])


@router.get("/auth/status", response_model=ApiResponse)
def auth_status() -> ApiResponse:
    status = build_auth_configuration_status()
    return ApiResponse(
        success=True,
        data=serialize_model(status),
        error=None,
        metadata=build_metadata(),
    )


@router.get("/me", response_model=ApiResponse)
def current_user(current_user: CurrentUser = Depends(require_current_user)) -> ApiResponse:
    return ApiResponse(
        success=True,
        data=serialize_model(current_user),
        error=None,
        metadata=build_metadata(),
    )
