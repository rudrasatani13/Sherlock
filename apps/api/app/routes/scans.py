from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.scans import ScansModuleStatus

router = APIRouter(prefix="/scans", tags=["scans"])


@router.get("", response_model=ApiResponse)
def scans_placeholder() -> ApiResponse:
    details = ScansModuleStatus(
        future_capabilities=["scan request contracts", "scan status", "queue handoff", "worker result ingestion"],
        disabled_capabilities=[
            "scanner execution",
            "public scan creation",
            "queue workers",
            "active scan persistence",
            "ownership verification bypasses",
        ],
    )
    raise NotImplementedApiError("scans", serialize_model(details))
