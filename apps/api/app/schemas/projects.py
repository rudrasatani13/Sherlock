from __future__ import annotations

from .common import ModuleStatus


class ProjectsModuleStatus(ModuleStatus):
    module: str = "projects"
    status: str = "placeholder_only"
    purpose: str = "Future project/workspace organization for authenticated Sherlock customers."
    future_phase: str = "Phase 11 authentication and future persistence integration"
