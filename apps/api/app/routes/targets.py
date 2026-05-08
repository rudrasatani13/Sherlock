from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.targets import TargetSetupContract, TargetsModuleStatus

router = APIRouter(prefix="/targets", tags=["targets"])


@router.get("", response_model=ApiResponse)
def targets_placeholder() -> ApiResponse:
    details = TargetsModuleStatus(
        available_endpoints=["GET /api/v0/targets"],
        future_capabilities=["safe target setup metadata", "target scope state", "ownership verification status"],
        disabled_capabilities=[
            "active API persistence",
            "target ownership verification logic",
            "SSRF protection implementation",
            "public scanning",
            "secret storage",
            "scanner execution",
        ],
    )
    payload = serialize_model(details)
    payload["setup_contract"] = serialize_model(TargetSetupContract())
    raise NotImplementedApiError("targets", payload)
