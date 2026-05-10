from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .common import ModuleStatus


class FindingsModuleStatus(ModuleStatus):
    module: str = "findings"
    status: str = "findings_system_foundation"
    purpose: str = "Phase 17 findings system contract for structured candidates, reviewed findings, statuses, categories, severity, confidence, evidence, and fix guidance."
    future_phase: str = "Future production findings retrieval after auth, persistence, and access controls"


class FindingStatusEntry(BaseModel):
    status: str
    display_name: str


class FindingCategoryEntry(BaseModel):
    category: str
    display_name: str


class FindingsContract(BaseModel):
    """Static Phase 17 findings contract metadata.

    This is not a persistence schema and does not return customer findings.
    """

    current_behavior: str = "Static contract metadata only. No route reads or writes finding records."
    package: str = "packages.findings_system"
    statuses: List[FindingStatusEntry] = Field(default_factory=list)
    future_statuses: List[str] = Field(default_factory=list)
    severities: List[str] = Field(default_factory=list)
    confidences: List[str] = Field(default_factory=list)
    categories: List[FindingCategoryEntry] = Field(default_factory=list)
    required_fields: List[str] = Field(default_factory=lambda: [
        "title",
        "category",
        "severity",
        "confidence",
        "description",
        "business_impact",
        "evidence_summary",
        "reproduction_steps",
        "fix_recommendation",
        "status",
    ])
    validation_rules: List[str] = Field(default_factory=lambda: [
        "critical/high findings require evidence summary",
        "critical/high findings require fix recommendation",
        "critical findings require strong evidence marker or manual review",
        "false_positive requires a reason",
        "evidence must be redacted and appropriate for report display by default",
        "unknown categories normalize to other_unknown",
    ])
    disabled_capabilities: List[str] = Field(default_factory=lambda: [
        "active finding persistence",
        "database reads or writes",
        "customer finding retrieval",
        "report generation",
        "PDF export",
        "public scan execution",
    ])
