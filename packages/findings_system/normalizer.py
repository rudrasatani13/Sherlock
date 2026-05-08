"""Normalize evaluator/scanner observations into Phase 17 findings."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

from .categories import CATEGORY_DISPLAY_NAMES, normalize_category
from .evidence import make_evidence_item, summarize_evidence
from .models import Finding, FindingCandidate, display_title_for_category, stable_finding_id
from .recommendations import recommendation_for_category
from .severity import CONFIDENCE_HIGH, SEVERITY_CRITICAL, normalize_confidence, normalize_severity
from .statuses import STATUS_NEEDS_REVIEW, STATUS_OPEN, normalize_status


CUSTOMER_IMPACT: dict[str, str] = {
    "prompt_injection": (
        "A user-controlled instruction may change how the AI surface follows policy or business rules. "
        "If confirmed, this can weaken launch controls and make related data or tool risks easier to trigger."
    ),
    "system_prompt_leakage": (
        "Hidden instructions or operational details may be exposed to users. This can reveal implementation details "
        "and make future bypass attempts easier, even when no secret is present."
    ),
    "sensitive_data_leakage": (
        "The AI surface may disclose data that the requester should not receive. If confirmed, this can create "
        "privacy, contractual, and trust risk for the SaaS team."
    ),
    "rag_data_leakage": (
        "Retrieved content may be shown outside its intended authorization boundary. If confirmed, document-level "
        "permissions and tenant isolation need review before launch."
    ),
    "indirect_prompt_injection": (
        "Untrusted retrieved or external content may influence the AI application as if it were an instruction. "
        "This can affect data access, tool use, or user-facing answers."
    ),
    "tool_function_abuse": (
        "The AI surface may prepare or claim a risky tool action without the expected permission boundary. "
        "If confirmed, customer data or workflow state could be changed incorrectly."
    ),
    "unsafe_output_handling": (
        "Model output may be rendered or forwarded in a way that could execute unsafe content. The impact depends "
        "on the UI or downstream renderer that consumes the output."
    ),
    "cost_abuse_unbounded_consumption": (
        "The AI surface may allow excessive model output, retries, or long-running behavior. This can create cost, "
        "availability, and abuse risk if execution limits are missing."
    ),
    "other_unknown": (
        "The observation needs human review before Sherlock can assign a specific business impact or customer-facing claim."
    ),
}


def candidates_from_evaluator_output(payload: Dict[str, Any] | Iterable[Dict[str, Any]]) -> List[FindingCandidate]:
    """Convert Phase 7 evaluator output into finding candidates.

    Safe or empty evaluator results do not produce findings. Ambiguous or
    high-impact results become candidates and may stay in needs_review status.
    """
    if isinstance(payload, dict):
        evaluations = payload.get("evaluations")
        if evaluations is None and "test_id" in payload:
            evaluations = [payload]
        source_scan_id = str(payload.get("source_scan_id") or "")
        affected_target = str(payload.get("source_target_name") or payload.get("target_name") or "")
    else:
        evaluations = list(payload)
        source_scan_id = ""
        affected_target = ""

    candidates: List[FindingCandidate] = []
    for evaluation in evaluations or []:
        if not isinstance(evaluation, dict):
            continue
        candidates.extend(
            candidates_from_evaluation(
                evaluation,
                source_scan_id=source_scan_id,
                affected_target=affected_target,
            )
        )
    return candidates


def candidates_from_evaluation(
    evaluation: Dict[str, Any],
    *,
    source_scan_id: str = "",
    affected_target: str = "",
) -> List[FindingCandidate]:
    """Convert one evaluator result into zero or more finding candidates."""
    verdict = str(evaluation.get("verdict") or "").lower()
    if verdict == "safe":
        return []

    matched_signals = [item for item in evaluation.get("matched_signals", []) if isinstance(item, dict)]
    if not matched_signals and verdict not in {"needs_manual_review", "inconclusive", "error"}:
        return []
    if not matched_signals:
        matched_signals = [
            {
                "name": "manual_review_trigger",
                "group": evaluation.get("category") or "other_unknown",
                "severity": evaluation.get("severity") or "informational",
                "confidence": evaluation.get("confidence") or "low",
                "description": evaluation.get("reasoning_summary") or "Evaluator result requires manual review.",
                "evidence_count": 0,
            }
        ]

    evidence_items = [item for item in evaluation.get("evidence", []) if isinstance(item, dict)]
    candidates: List[FindingCandidate] = []
    for signal in matched_signals:
        signal_name = str(signal.get("name") or "evaluator_signal")
        signal_group = str(signal.get("group") or evaluation.get("category") or "other_unknown")
        evidence_text = _evidence_for_signal(evidence_items, signal_group, signal_name)
        category = normalize_category(evaluation.get("category") or signal_group)
        severity_hint = normalize_severity(signal.get("severity") or evaluation.get("severity"))
        confidence_hint = normalize_confidence(signal.get("confidence") or evaluation.get("confidence"))
        candidates.append(
            FindingCandidate(
                category=category,
                detector_name=signal_name,
                severity_hint=severity_hint,
                confidence_hint=confidence_hint,
                observed_behavior=_observed_behavior(signal, evaluation),
                evidence_snippet=evidence_text,
                redacted_evidence=summarize_evidence(evidence_text),
                test_case_id=str(evaluation.get("test_id") or ""),
                needs_manual_review=bool(evaluation.get("needs_manual_review")) or verdict in {"needs_manual_review", "inconclusive", "error"},
                reason=", ".join(str(item) for item in evaluation.get("manual_review_reasons", []) if item)
                or str(evaluation.get("reasoning_summary") or ""),
                affected_target=affected_target,
                source_scan_id=source_scan_id,
                evaluator_signals=[dict(signal)],
                metadata={
                    "source_verdict": verdict,
                    "evaluator_version": evaluation.get("evaluator_version"),
                    "evaluated_at": evaluation.get("evaluated_at"),
                    "strong_evidence": bool(evidence_text) and confidence_hint == CONFIDENCE_HIGH,
                },
            )
        )
    return candidates


def finding_from_candidate(candidate: FindingCandidate, *, status: str | None = None) -> Finding:
    """Build a validated finalized finding from a candidate."""
    normalized_status = normalize_status(status or (STATUS_NEEDS_REVIEW if candidate.needs_manual_review else STATUS_OPEN))
    evidence_source = candidate.redacted_evidence or candidate.evidence_snippet or candidate.observed_behavior
    evidence_item = make_evidence_item(
        signal=candidate.detector_name,
        snippet=evidence_source,
        source_test_id=candidate.test_case_id,
        strong_evidence=bool(candidate.redacted_evidence) and candidate.confidence_hint == CONFIDENCE_HIGH,
    )
    category_name = CATEGORY_DISPLAY_NAMES[normalize_category(candidate.category)]
    title = display_title_for_category(candidate.category, candidate.detector_name)
    description = (
        f"Sherlock observed {candidate.observed_behavior}. This candidate is mapped to {category_name} "
        "and should be reviewed against the tested scope before customer-facing use."
    )
    finding = Finding(
        finding_id=stable_finding_id(title, candidate.category, candidate.affected_target, ",".join(candidate.source_test_ids)),
        title=title,
        category=candidate.category,
        severity=candidate.severity_hint,
        confidence=candidate.confidence_hint,
        status=normalized_status,
        description=description,
        business_impact=CUSTOMER_IMPACT[normalize_category(candidate.category)],
        evidence_summary=evidence_item.summary,
        evidence_items=[evidence_item] if evidence_item.summary else [],
        reproduction_steps=format_reproduction_steps(candidate),
        fix_recommendation=recommendation_for_category(candidate.category),
        affected_target=candidate.affected_target,
        source_scan_id=candidate.source_scan_id,
        source_test_ids=list(candidate.source_test_ids),
        evaluator_signals=list(candidate.evaluator_signals),
        manual_review_required=candidate.needs_manual_review or candidate.severity_hint == SEVERITY_CRITICAL,
        manual_review_notes="",
        metadata={
            "phase": "phase_17_findings_system_foundation",
            "candidate_reason": candidate.reason,
            "source_candidate": candidate.to_dict(),
            "strong_evidence": bool(candidate.metadata.get("strong_evidence")),
        },
    )
    return finding


def findings_from_candidates(candidates: Iterable[FindingCandidate]) -> List[Finding]:
    """Group, merge, finalize, and sort candidates into findings."""
    from .grouping import merge_candidate_group, group_duplicate_candidates, sort_findings

    findings = [
        finding_from_candidate(merge_candidate_group(group))
        for group in group_duplicate_candidates(candidates).values()
    ]
    return sort_findings(findings)


def format_reproduction_steps(candidate: FindingCandidate) -> List[str]:
    steps = []
    if candidate.test_case_id:
        steps.append(f"Run Sherlock test case {candidate.test_case_id} against the affected target inside the approved scan scope.")
    else:
        steps.append("Re-run the same approved scanner or manual test condition against the affected target.")
    steps.append("Compare the target response with the expected safe behavior for the category.")
    steps.append("Review the redacted evidence summary and confirm impact before customer-facing reporting.")
    return steps


def _evidence_for_signal(evidence_items: List[Dict[str, Any]], signal_group: str, signal_name: str) -> str:
    for item in evidence_items:
        signal = str(item.get("signal") or "")
        if signal in {signal_group, signal_name}:
            return str(item.get("redacted_snippet") or item.get("snippet") or "")
    if evidence_items:
        first = evidence_items[0]
        return str(first.get("redacted_snippet") or first.get("snippet") or "")
    return ""


def _observed_behavior(signal: Dict[str, Any], evaluation: Dict[str, Any]) -> str:
    description = str(signal.get("description") or "").strip()
    if description:
        return description[:1].lower() + description[1:]
    summary = str(evaluation.get("reasoning_summary") or "").strip()
    if summary:
        return summary[:1].lower() + summary[1:]
    return "an evaluator signal that requires review"
