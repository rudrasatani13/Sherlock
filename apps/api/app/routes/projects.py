from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse, serialize_model
from ..schemas.projects import ProjectSetupContract, ProjectsModuleStatus

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ApiResponse)
def projects_placeholder() -> ApiResponse:
    details = ProjectsModuleStatus(
        available_endpoints=["GET /api/v0/projects"],
        future_capabilities=["project setup metadata", "project selection", "project target grouping"],
        disabled_capabilities=[
            "active API persistence",
            "authentication",
            "authorization",
            "database writes from dashboard UI",
            "real production project persistence",
        ],
    )
    payload = serialize_model(details)
    payload["setup_contract"] = serialize_model(ProjectSetupContract())
    raise NotImplementedApiError("projects", payload)
