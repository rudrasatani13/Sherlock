from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse
from ..schemas.findings import FindingsModuleStatus

router = APIRouter(prefix="/findings", tags=["findings"])


@router.get("", response_model=ApiResponse)
def findings_placeholder() -> ApiResponse:
    details = FindingsModuleStatus(
        future_capabilities=["reviewed findings", "severity", "confidence", "status", "retest state"],
        disabled_capabilities=["finding persistence", "automatic public findings", "report generation"],
    )
    raise NotImplementedApiError("findings", details.dict())
