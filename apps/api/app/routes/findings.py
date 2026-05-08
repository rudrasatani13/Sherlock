from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError, build_metadata
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.findings import (
    FindingCategoryEntry,
    FindingsContract,
    FindingsModuleStatus,
    FindingStatusEntry,
)

router = APIRouter(prefix="/findings", tags=["findings"])


def _build_findings_contract() -> dict:
    from packages.findings_system.categories import CATEGORY_DISPLAY_NAMES
    from packages.findings_system.severity import CONFIDENCES, SEVERITIES
    from packages.findings_system.statuses import FUTURE_STATUSES, STATUS_DISPLAY_NAMES, STATUSES

    contract = FindingsContract(
        statuses=[
            FindingStatusEntry(status=status, display_name=STATUS_DISPLAY_NAMES[status])
            for status in STATUSES
        ],
        future_statuses=list(FUTURE_STATUSES),
        severities=list(SEVERITIES),
        confidences=list(CONFIDENCES),
        categories=[
            FindingCategoryEntry(category=category, display_name=display_name)
            for category, display_name in CATEGORY_DISPLAY_NAMES.items()
        ],
    )
    return serialize_model(contract)


@router.get("", response_model=ApiResponse)
def findings_placeholder() -> ApiResponse:
    details = FindingsModuleStatus(
        available_endpoints=["GET /api/v0/findings", "GET /api/v0/findings/schema"],
        future_capabilities=[
            "reviewed findings retrieval after auth and persistence exist",
            "manual review workflows",
            "retest state integration",
            "Phase 18 report consumption",
        ],
        disabled_capabilities=[
            "active finding persistence",
            "automatic public findings",
            "database reads or writes",
            "report generation",
            "PDF export",
        ],
    )
    payload = serialize_model(details)
    payload["findings_contract"] = _build_findings_contract()
    raise NotImplementedApiError("findings", payload)


@router.get("/schema", response_model=ApiResponse)
def findings_schema() -> ApiResponse:
    """Return the static Phase 17 findings contract.

    This endpoint does not return stored findings, customer evidence, scan
    output, report data, or database records.
    """
    return ApiResponse(
        success=True,
        data={
            "phase": "Phase 17 Findings System foundation",
            "findings_contract": _build_findings_contract(),
            "note": "Static schema metadata only. Active findings persistence and report generation are not implemented.",
        },
        error=None,
        metadata=build_metadata(),
    )
