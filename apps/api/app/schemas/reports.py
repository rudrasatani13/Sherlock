from __future__ import annotations

from .common import ModuleStatus


class ReportsModuleStatus(ModuleStatus):
    module: str = "reports"
    status: str = "placeholder_only"
    purpose: str = "Future report metadata and web report access contracts after findings are reviewed."
    future_phase: str = "Phase 18 web report"
