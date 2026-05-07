from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.verification import VerificationModuleStatus

router = APIRouter(prefix="/verification", tags=["verification"])


@router.get("", response_model=ApiResponse)
def verification_placeholder() -> ApiResponse:
    details = VerificationModuleStatus(
        future_capabilities=["ownership verification challenge records", "verification review state"],
        disabled_capabilities=["production verification logic", "public scan unlocking", "active API persistence"],
    )
    raise NotImplementedApiError("verification", serialize_model(details))
