from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.verification import VerificationContract, VerificationModuleStatus

router = APIRouter(prefix="/verification", tags=["verification"])


@router.get("", response_model=ApiResponse)
def verification_placeholder() -> ApiResponse:
    details = VerificationModuleStatus(
        future_capabilities=[
            "ownership verification challenge creation",
            "DNS TXT record verification",
            "HTML meta tag verification",
            "well-known file verification",
            "manual authorization review",
            "chatbot/API challenge verification",
            "verification status tracking",
            "challenge token generation and hashing",
        ],
        disabled_capabilities=[
            "production DNS/HTTP/chatbot verification checks",
            "active API persistence of verification records",
            "public scan unlocking",
            "SSRF-safe network requests",
            "rate-limited verification attempts",
        ],
    )
    payload = serialize_model(details)
    payload["verification_contract"] = serialize_model(VerificationContract())
    raise NotImplementedApiError("verification", payload)
