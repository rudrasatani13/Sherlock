from __future__ import annotations

from .common import ModuleStatus


class TargetsModuleStatus(ModuleStatus):
    module: str = "targets"
    status: str = "placeholder_only"
    purpose: str = "Future target registration and authorized target metadata."
    future_phase: str = "Phase 14 ownership verification"
