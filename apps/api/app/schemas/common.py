from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None


class ResponseMetadata(BaseModel):
    api_version: str
    phase: str
    environment: str


class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ModuleStatus(BaseModel):
    module: str
    status: str
    purpose: str
    future_phase: Optional[str] = None
    available_endpoints: List[str] = Field(default_factory=list)
    future_capabilities: List[str] = Field(default_factory=list)
    disabled_capabilities: List[str] = Field(default_factory=list)


def serialize_model(model: BaseModel) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()
