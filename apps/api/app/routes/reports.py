from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.reports import ReportsModuleStatus

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=ApiResponse)
def reports_placeholder() -> ApiResponse:
    details = ReportsModuleStatus(
        future_capabilities=["web report metadata", "report access status", "finding summaries"],
        disabled_capabilities=["real report generation", "PDF export", "active report persistence", "admin panel"],
    )
    raise NotImplementedApiError("reports", serialize_model(details))
