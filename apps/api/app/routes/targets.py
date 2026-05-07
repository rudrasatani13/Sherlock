from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse
from ..schemas.targets import TargetsModuleStatus

router = APIRouter(prefix="/targets", tags=["targets"])


@router.get("", response_model=ApiResponse)
def targets_placeholder() -> ApiResponse:
    details = TargetsModuleStatus(
        future_capabilities=["target metadata", "target scope state", "ownership verification status"],
        disabled_capabilities=[
            "database persistence",
            "target ownership verification logic",
            "SSRF protection implementation",
            "public scanning",
        ],
    )
    raise NotImplementedApiError("targets", details.dict())
