from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.scans import ScanQueueContract, ScansModuleStatus

router = APIRouter(prefix="/scans", tags=["scans"])


@router.get("", response_model=ApiResponse)
def scans_placeholder() -> ApiResponse:
    module_status = ScansModuleStatus(
        future_capabilities=[
            "scan job creation (authenticated + verified targets only)",
            "scan job status queries",
            "scan job cancellation",
            "queue worker handoff",
            "worker result ingestion",
        ],
        disabled_capabilities=[
            "public scan creation",
            "production queue deployment",
            "active scan persistence",
            "ownership verification bypasses",
            "scanner execution from API routes",
            "real network scanning",
        ],
    )
    queue_contract = ScanQueueContract()
    details = serialize_model(module_status)
    details["queue_contract"] = serialize_model(queue_contract)
    raise NotImplementedApiError("scans", details)
