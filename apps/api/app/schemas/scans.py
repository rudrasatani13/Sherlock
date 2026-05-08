from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field

from .common import ModuleStatus


class ScansModuleStatus(ModuleStatus):
    module: str = "scans"
    status: str = "scan_types_and_limits_foundation"
    purpose: str = "Phase 16 scan types, limits, and plan tier foundation. Scan jobs are dispatched through background workers with bounded modes and validated limits."
    future_phase: str = "Future production queue deployment after auth, verification, SSRF protection, and rate limits"


class JobTypeEntry(BaseModel):
    job_type: str
    purpose: str
    phase_15_status: str


class JobStatusEntry(BaseModel):
    status: str
    description: str


class ScanTypeEntry(BaseModel):
    """Phase 16 scan type metadata for API contracts."""
    scan_type: str
    display_name: str
    description: str
    max_tests: int
    timeout_seconds: int
    max_concurrency: int
    max_response_chars_per_test: int
    included_categories: List[str]
    requires_verified_target: bool
    requires_manual_review: bool
    report_level: str
    enabled: bool
    future_plan_availability: List[str]


class PlanTierEntry(BaseModel):
    """Phase 16 plan tier placeholder for API contracts."""
    tier: str
    display_name: str
    description: str
    allowed_scan_types: List[str]
    monthly_scan_limit: int
    max_projects: int
    retest_allowance: int
    pdf_export_available: bool
    web_report_available: bool
    enabled: bool
    billing_placeholder: str


class ScanQueueContract(BaseModel):
    """Phase 15 queue/worker contract metadata for the scans placeholder route."""
    current_behavior: str = "No route creates scan jobs or starts workers. The queue and worker system is a local foundation under packages/worker_system."
    job_types: List[JobTypeEntry] = Field(default_factory=lambda: [
        JobTypeEntry(job_type="scan.run", purpose="Execute a scan against a verified target", phase_15_status="mock_only"),
        JobTypeEntry(job_type="scan.evaluate", purpose="Run evaluator on scan results", phase_15_status="placeholder"),
        JobTypeEntry(job_type="scan.summarize", purpose="Summarize scan findings", phase_15_status="placeholder"),
        JobTypeEntry(job_type="report.prepare_placeholder", purpose="Prepare report draft", phase_15_status="placeholder"),
    ])
    job_lifecycle_states: List[JobStatusEntry] = Field(default_factory=lambda: [
        JobStatusEntry(status="queued", description="Job is waiting in the queue"),
        JobStatusEntry(status="running", description="Worker has picked up the job"),
        JobStatusEntry(status="completed", description="Job finished successfully"),
        JobStatusEntry(status="failed", description="Job encountered an error"),
        JobStatusEntry(status="cancelled", description="Job was cancelled before completion"),
        JobStatusEntry(status="timed_out", description="Job exceeded its timeout"),
        JobStatusEntry(status="blocked_unverified", description="Blocked because target is not verified"),
        JobStatusEntry(status="blocked_unsafe", description="Blocked by a safety gate"),
    ])
    safety_gates: List[str] = Field(default_factory=lambda: [
        "queue_enabled",
        "target_verified",
        "job_type_allowed",
        "target_url_safe",
        "no_secrets_in_payload",
        "limits",
        "scan_type_limits",
    ])
    future_endpoints: List[Dict[str, str]] = Field(default_factory=lambda: [
        {"method": "POST", "path": "/api/v0/scans", "purpose": "Create a scan job (future authenticated + verified)"},
        {"method": "GET", "path": "/api/v0/scans/{scan_id}", "purpose": "Get scan job status"},
        {"method": "POST", "path": "/api/v0/scans/{scan_id}/cancel", "purpose": "Cancel a queued or running scan job"},
        {"method": "GET", "path": "/api/v0/scans/types", "purpose": "List available scan types and limits"},
        {"method": "GET", "path": "/api/v0/scans/limits", "purpose": "Get current scan limits and plan tier info"},
    ])
    forbidden_payload_fields: List[str] = Field(default_factory=lambda: [
        "api_key", "api_secret", "bearer_token", "access_token", "refresh_token",
        "password", "private_key", "secret_key", "cookie", "session_token",
        "authorization_header", "raw_header", "credential",
    ])

