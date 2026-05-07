from __future__ import annotations

from fastapi import APIRouter

from ..errors import NotImplementedApiError
from ..schemas.common import ApiResponse
from ..schemas.projects import ProjectsModuleStatus

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ApiResponse)
def projects_placeholder() -> ApiResponse:
    details = ProjectsModuleStatus(
        future_capabilities=["project records", "project targets", "team/account ownership"],
        disabled_capabilities=["database persistence", "authentication", "authorization", "dashboard integration"],
    )
    raise NotImplementedApiError("projects", details.dict())
