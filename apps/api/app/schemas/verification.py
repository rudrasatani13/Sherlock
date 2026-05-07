from __future__ import annotations

from .common import ModuleStatus


class VerificationModuleStatus(ModuleStatus):
    module: str = "verification"
    status: str = "placeholder_only"
    purpose: str = "Future target ownership verification records and checks before any public scanning."
    future_phase: str = "Phase 14 ownership verification"
