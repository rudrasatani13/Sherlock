"""Duplicate grouping, merging, and sorting helpers for Phase 17 findings."""
from __future__ import annotations

import hashlib
import re
from typing import Dict, Iterable, List

from .categories import normalize_category
from .evidence import evidence_summary, make_evidence_item
from .models import Finding, FindingCandidate, stable_finding_id
from .recommendations import recommendation_for_category
from .severity import (
    CONFIDENCE_RANK,
    SEVERITY_RANK,
    normalize_confidence,
    normalize_severity,
    strongest_confidence,
    strongest_severity,
)
from .statuses import STATUS_NEEDS_REVIEW


STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "by",
    "for",
    "in",
    "into",
    "of",
    "or",
    "the",
    "to",
    "with",
}


def duplicate_group_key(value: FindingCandidate | Finding) -> str:
    """Group same category/target/similar title or evidence signal together."""
    category = normalize_category(value.category)
    target = _fingerprint(getattr(value, "affected_target", ""))
    if isinstance(value, FindingCandidate):
        signal = _fingerprint(value.detector_name)
        text = value.observed_behavior or value.redacted_evidence
    else:
        signal = _fingerprint(value.title)
        text = value.evidence_summary or value.description
    text_fingerprint = _fingerprint(text)
    seed = "|".join((category, target, signal, text_fingerprint[:48]))
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def group_duplicate_candidates(candidates: Iterable[FindingCandidate]) -> Dict[str, List[FindingCandidate]]:
    groups: Dict[str, List[FindingCandidate]] = {}
    for candidate in candidates:
        key = duplicate_group_key(candidate)
        groups.setdefault(key, []).append(candidate)
    return groups


def merge_candidate_group(candidates: Iterable[FindingCandidate]) -> FindingCandidate:
    group = list(candidates)
    if not group:
        raise ValueError("cannot merge empty candidate group")
    primary = group[0]
    severity = strongest_severity(candidate.severity_hint for candidate in group)
    confidence = strongest_confidence(candidate.confidence_hint for candidate in group)
    source_test_ids: List[str] = []
    evaluator_signals = []
    evidence_parts: List[str] = []
    reasons: List[str] = []
    for candidate in group:
        source_test_ids.extend(candidate.source_test_ids)
        evaluator_signals.extend(candidate.evaluator_signals)
        if candidate.redacted_evidence and candidate.redacted_evidence not in evidence_parts:
            evidence_parts.append(candidate.redacted_evidence)
        if candidate.reason and candidate.reason not in reasons:
            reasons.append(candidate.reason)
    merged = FindingCandidate(
        category=primary.category,
        detector_name=primary.detector_name,
        severity_hint=severity,
        confidence_hint=confidence,
        observed_behavior=primary.observed_behavior,
        evidence_snippet=" | ".join(evidence_parts),
        redacted_evidence=evidence_summary(
            [
                make_evidence_item(
                    signal=primary.detector_name,
                    snippet=part,
                    strong_evidence=confidence == "high",
                )
                for part in evidence_parts
            ]
        ),
        test_case_id=primary.test_case_id,
        needs_manual_review=any(candidate.needs_manual_review for candidate in group),
        reason="; ".join(reasons),
        affected_target=primary.affected_target,
        source_scan_id=primary.source_scan_id,
        source_test_ids=sorted(set(source_test_ids)),
        evaluator_signals=evaluator_signals,
        metadata={
            "merged": len(group) > 1,
            "merged_count": len(group),
            "duplicate_group_key": duplicate_group_key(primary),
            "source_candidate_test_ids": sorted(set(source_test_ids)),
            "strong_evidence": any(candidate.metadata.get("strong_evidence") for candidate in group),
        },
    )
    return merged


def merge_similar_findings(findings: Iterable[Finding]) -> List[Finding]:
    """Merge finalized findings that share a duplicate group key."""
    groups: Dict[str, List[Finding]] = {}
    for finding in findings:
        groups.setdefault(finding.duplicate_group_key or duplicate_group_key(finding), []).append(finding)

    merged: List[Finding] = []
    for group in groups.values():
        if len(group) == 1:
            merged.append(group[0])
            continue
        primary = group[0]
        severity = strongest_severity(finding.severity for finding in group)
        confidence = strongest_confidence(finding.confidence for finding in group)
        source_test_ids = sorted({test_id for finding in group for test_id in finding.source_test_ids})
        evidence_items = []
        evaluator_signals = []
        for finding in group:
            evidence_items.extend(finding.evidence_items)
            evaluator_signals.extend(finding.evaluator_signals)
        merged.append(
            Finding(
                finding_id=stable_finding_id(primary.title, primary.category, primary.affected_target, ",".join(source_test_ids)),
                title=primary.title,
                category=primary.category,
                severity=severity,
                confidence=confidence,
                status=STATUS_NEEDS_REVIEW if any(item.manual_review_required for item in group) else primary.status,
                description=primary.description,
                business_impact=primary.business_impact,
                evidence_summary=evidence_summary(evidence_items, primary.evidence_summary),
                evidence_items=evidence_items,
                reproduction_steps=primary.reproduction_steps,
                fix_recommendation=primary.fix_recommendation or recommendation_for_category(primary.category),
                affected_target=primary.affected_target,
                source_scan_id=primary.source_scan_id,
                source_test_ids=source_test_ids,
                evaluator_signals=evaluator_signals,
                duplicate_group_key=primary.duplicate_group_key or duplicate_group_key(primary),
                manual_review_required=any(item.manual_review_required for item in group),
                metadata={**primary.metadata, "merged": True, "merged_count": len(group)},
            )
        )
    return sort_findings(merged)


def sort_findings(findings: Iterable[Finding]) -> List[Finding]:
    """Sort by severity, confidence, category, then title."""
    return sorted(
        list(findings),
        key=lambda finding: (
            -SEVERITY_RANK[normalize_severity(finding.severity)],
            -CONFIDENCE_RANK[normalize_confidence(finding.confidence)],
            finding.category,
            finding.title.lower(),
        ),
    )


def _fingerprint(value: str) -> str:
    tokens = re.findall(r"[a-z0-9]+", (value or "").lower())
    useful = [token for token in tokens if token not in STOPWORDS]
    return "_".join(useful[:8])
