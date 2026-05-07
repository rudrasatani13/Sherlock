from __future__ import annotations

from .common import ModuleStatus


class FindingsModuleStatus(ModuleStatus):
    module: str = "findings"
    status: str = "placeholder_only"
    purpose: str = "Future reviewed finding records based on methodology, evidence, severity, confidence, and status."
    future_phase: str = "Phase 17 findings system"
