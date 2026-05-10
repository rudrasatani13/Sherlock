from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError, build_metadata
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.reports import PdfExportContract, ReportsContract, ReportsModuleStatus

router = APIRouter(prefix="/reports", tags=["reports"])


def _build_reports_contract() -> dict:
    from packages.report_system.models import LAUNCH_READINESS_VERDICTS, REPORT_STATUSES, REPORT_TYPES

    contract = ReportsContract(
        report_statuses=list(REPORT_STATUSES),
        report_types=list(REPORT_TYPES),
        launch_readiness_verdicts=list(LAUNCH_READINESS_VERDICTS),
    )
    return serialize_model(contract)


def _build_pdf_export_contract() -> dict:
    from packages.pdf_export.models import PDF_EXPORT_STATUSES, PDF_EXPORT_TYPES

    contract = PdfExportContract(
        export_statuses=list(PDF_EXPORT_STATUSES),
        export_types=list(PDF_EXPORT_TYPES),
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
            "production PDF delivery after secure storage and access control exist",
        ],
        disabled_capabilities=[
            "real customer report retrieval",
            "production PDF export for real customer reports",
            "active report persistence",
            "report database writes",
            "billing gates",
            "admin panel",
            "public report sharing links",
        ],
    )
    payload = serialize_model(details)
    payload["reports_contract"] = _build_reports_contract()
    payload["pdf_export_contract"] = _build_pdf_export_contract()
    raise NotImplementedApiError("reports", payload)


@router.get("/schema", response_model=ApiResponse)
def reports_schema() -> ApiResponse:
    """Return static Phase 18 report and Phase 19 PDF export contracts.

    This endpoint does not return stored reports, customer evidence, scan
    output, share links, PDF assets, or database records.
    """
    return ApiResponse(
        success=True,
        data={
            "phase": "Phase 19 PDF Report Export foundation",
            "reports_contract": _build_reports_contract(),
            "pdf_export_contract": _build_pdf_export_contract(),
            "note": "Static schema metadata only. Local/demo print-ready HTML export support exists in packages.pdf_export, but active report persistence, customer report retrieval, public sharing, production PDF delivery, storage, billing, and database writes are not implemented.",
        },
        error=None,
        metadata=build_metadata(),
    )
