from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError, build_metadata
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.reports import ReportsContract, ReportsModuleStatus

router = APIRouter(prefix="/reports", tags=["reports"])


def _build_reports_contract() -> dict:
    from packages.report_system.models import LAUNCH_READINESS_VERDICTS, REPORT_STATUSES, REPORT_TYPES

    contract = ReportsContract(
        report_statuses=list(REPORT_STATUSES),
        report_types=list(REPORT_TYPES),
        launch_readiness_verdicts=list(LAUNCH_READINESS_VERDICTS),
    )
    return serialize_model(contract)


@router.get("", response_model=ApiResponse)
def reports_placeholder() -> ApiResponse:
    details = ReportsModuleStatus(
        available_endpoints=["GET /api/v0/reports", "GET /api/v0/reports/schema"],
        future_capabilities=[
            "authenticated report retrieval after auth and persistence exist",
            "report access status",
            "report sharing controls in a future phase",
            "PDF export in Phase 19",
        ],
        disabled_capabilities=[
            "real customer report retrieval",
            "PDF export",
            "active report persistence",
            "report database writes",
            "billing gates",
            "admin panel",
            "public report sharing links",
        ],
    )
    payload = serialize_model(details)
    payload["reports_contract"] = _build_reports_contract()
    raise NotImplementedApiError("reports", payload)


@router.get("/schema", response_model=ApiResponse)
def reports_schema() -> ApiResponse:
    """Return the static Phase 18 report contract.

    This endpoint does not return stored reports, customer evidence, scan
    output, share links, PDF assets, or database records.
    """
    return ApiResponse(
        success=True,
        data={
            "phase": "Phase 18 Web Report foundation",
            "reports_contract": _build_reports_contract(),
            "note": "Static schema metadata only. Active report persistence, report retrieval, sharing, and PDF export are not implemented.",
        },
        error=None,
        metadata=build_metadata(),
    )
