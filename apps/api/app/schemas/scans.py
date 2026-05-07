from __future__ import annotations

from .common import ModuleStatus


class ScansModuleStatus(ModuleStatus):
    module: str = "scans"
    status: str = "placeholder_only"
    purpose: str = "Future scan request, scan status, and worker handoff contracts."
    future_phase: str = "Phase 15 queue workers after auth, target verification, SSRF protection, and rate limits"
