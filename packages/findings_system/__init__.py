"""Phase 17 Findings System foundation for PowerDetect Sherlock."""
from __future__ import annotations

from .categories import CATEGORY_DISPLAY_NAMES, KNOWN_CATEGORIES, normalize_category
from .evidence import EvidenceItem, redact_evidence_text, summarize_evidence
from .grouping import (
    duplicate_group_key,
    group_duplicate_candidates,
    merge_candidate_group,
    merge_similar_findings,
    sort_findings,
)
from .models import Finding, FindingCandidate, FindingValidationError, validate_finding
from .normalizer import (
    candidates_from_evaluation,
    candidates_from_evaluator_output,
    finding_from_candidate,
    findings_from_candidates,
)
from .recommendations import RECOMMENDATION_TEMPLATES, recommendation_for_category
from .severity import CONFIDENCES, SEVERITIES
from .statuses import FUTURE_STATUSES, STATUSES


FINDINGS_SYSTEM_VERSION = "phase_17_findings_system_v0.1"

__all__ = [
    "CATEGORY_DISPLAY_NAMES",
    "CONFIDENCES",
    "EvidenceItem",
    "FINDINGS_SYSTEM_VERSION",
    "FUTURE_STATUSES",
    "Finding",
    "FindingCandidate",
    "FindingValidationError",
    "KNOWN_CATEGORIES",
    "RECOMMENDATION_TEMPLATES",
    "SEVERITIES",
    "STATUSES",
    "candidates_from_evaluation",
    "candidates_from_evaluator_output",
    "duplicate_group_key",
    "finding_from_candidate",
    "findings_from_candidates",
    "group_duplicate_candidates",
    "merge_candidate_group",
    "merge_similar_findings",
    "normalize_category",
    "recommendation_for_category",
    "redact_evidence_text",
    "sort_findings",
    "summarize_evidence",
    "validate_finding",
]
