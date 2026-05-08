from __future__ import annotations

import unittest

from packages.findings_system import (
    EvidenceItem,
    Finding,
    FindingValidationError,
    candidates_from_evaluator_output,
    findings_from_candidates,
    group_duplicate_candidates,
    merge_candidate_group,
    recommendation_for_category,
    redact_evidence_text,
    sort_findings,
    summarize_evidence,
)
from packages.findings_system.categories import normalize_category
from packages.findings_system.evidence import contains_unredacted_sensitive_marker
from packages.findings_system.models import FindingCandidate
from packages.findings_system.severity import normalize_confidence, normalize_severity
from packages.findings_system.statuses import normalize_status


def _finding(
    *,
    severity: str = "medium",
    confidence: str = "medium",
    status: str = "open",
    evidence: bool = True,
    strong_evidence: bool = False,
    manual_review_required: bool = False,
    false_positive_reason: str = "",
) -> Finding:
    evidence_items = [
        EvidenceItem(
            signal="demo_signal",
            summary="The response exposed a redacted demo canary marker.",
            redacted_snippet="The response exposed [REDACTED_CANARY].",
            source_test_id="SHK-APL-RAG-001",
            strong_evidence=strong_evidence,
        )
    ] if evidence else []
    return Finding(
        finding_id="",
        title="RAG data leakage canary disclosure",
        category="rag_data_leakage",
        severity=severity,
        confidence=confidence,
        status=status,
        description="The model response included restricted demo document content during an approved test.",
        business_impact="Restricted retrieved content may be exposed outside the intended authorization boundary.",
        evidence_summary="The response exposed a redacted demo canary marker." if evidence else "",
        evidence_items=evidence_items,
        reproduction_steps=["Run the approved demo RAG leakage test case."],
        fix_recommendation="Add document-level authorization and retrieval filtering before model context assembly.",
        manual_review_required=manual_review_required,
        false_positive_reason=false_positive_reason,
    )


class FindingModelValidationTests(unittest.TestCase):
    def test_valid_finding_model_serializes(self) -> None:
        finding = _finding(severity="high", confidence="high", strong_evidence=True)
        data = finding.to_dict()
        self.assertTrue(data["finding_id"].startswith("shk_find_"))
        self.assertEqual(data["severity"], "high")
        self.assertEqual(data["confidence"], "high")
        self.assertEqual(data["status"], "open")
        self.assertEqual(data["category"], "rag_data_leakage")
        self.assertIn("accepted_risk_reason", data)

    def test_status_validation_and_aliases(self) -> None:
        self.assertEqual(normalize_status("needs_manual_review"), "needs_review")
        self.assertEqual(normalize_status("accepted risk"), "accepted_risk")
        with self.assertRaises(ValueError):
            normalize_status("inconclusive")

    def test_severity_and_confidence_validation(self) -> None:
        self.assertEqual(normalize_severity("Critical"), "critical")
        self.assertEqual(normalize_confidence("none"), "low")
        with self.assertRaises(ValueError):
            normalize_severity("emergency")
        with self.assertRaises(ValueError):
            normalize_confidence("certain")

    def test_critical_high_require_evidence_and_fix_guidance(self) -> None:
        with self.assertRaises(FindingValidationError):
            _finding(severity="high", confidence="high", evidence=False)
        with self.assertRaises(FindingValidationError):
            Finding(
                finding_id="",
                title="Sensitive data leakage token disclosure",
                category="sensitive_data_leakage",
                severity="high",
                confidence="high",
                status="open",
                description="The model returned a redacted token-like value during the approved test.",
                business_impact="Sensitive data may be exposed to a user without permission.",
                evidence_summary="Token-like value was returned in the model response.",
                evidence_items=[
                    EvidenceItem(
                        signal="token",
                        summary="Token-like value was returned in the model response.",
                        redacted_snippet="[REDACTED_TOKEN]",
                        strong_evidence=True,
                    )
                ],
                fix_recommendation="",
            )

    def test_critical_requires_strong_evidence_or_manual_review(self) -> None:
        with self.assertRaises(FindingValidationError):
            _finding(severity="critical", confidence="high", strong_evidence=False, manual_review_required=False)
        finding = _finding(severity="critical", confidence="high", strong_evidence=False, manual_review_required=True)
        self.assertTrue(finding.manual_review_required)

    def test_high_requires_strong_evidence_or_manual_review(self) -> None:
        with self.assertRaises(FindingValidationError):
            _finding(severity="high", confidence="medium", strong_evidence=False, manual_review_required=False)
        finding = _finding(severity="high", confidence="medium", strong_evidence=False, manual_review_required=True)
        self.assertTrue(finding.manual_review_required)

    def test_false_positive_requires_reason(self) -> None:
        with self.assertRaises(FindingValidationError):
            _finding(status="false_positive")
        finding = _finding(status="false_positive", false_positive_reason="Owner confirmed the value was synthetic fixture data.")
        self.assertEqual(finding.status, "false_positive")

    def test_vague_title_or_description_rejected(self) -> None:
        with self.assertRaises(FindingValidationError):
            Finding(
                finding_id="",
                title="Issue found",
                category="prompt_injection",
                severity="low",
                confidence="low",
                status="needs_review",
                description="Bad output",
                business_impact="Manual review is needed before assigning impact.",
                evidence_summary="",
                fix_recommendation="Review the observed behavior manually.",
            )


class CategoryEvidenceRecommendationTests(unittest.TestCase):
    def test_category_mapping(self) -> None:
        self.assertEqual(normalize_category("cost_abuse"), "cost_abuse_unbounded_consumption")
        self.assertEqual(normalize_category("sensitive_data_pattern"), "sensitive_data_leakage")
        self.assertEqual(normalize_category("unknown_detector"), "other_unknown")

    def test_evidence_redaction_and_summary(self) -> None:
        raw = (
            "Authorization: Bearer abcdef1234567890\n"
            "Cookie: sid=secret-value;\n"
            "The api_key=sk-test_1234567890abcdef and FAKE-CANARY-NOVA-042 were returned."
        )
        redacted = redact_evidence_text(raw)
        self.assertIn("[REDACTED_HEADER]", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)
        self.assertIn("[REDACTED_CANARY]", redacted)
        self.assertFalse(contains_unredacted_sensitive_marker(redacted))
        self.assertLessEqual(len(summarize_evidence(raw)), 280)

    def test_candidate_evidence_is_redacted_by_default(self) -> None:
        candidate = FindingCandidate(
            category="sensitive_data_leakage",
            detector_name="assigned_secret",
            severity_hint="high",
            confidence_hint="medium",
            observed_behavior="response contained a secret-like assignment.",
            evidence_snippet="The api_key=sk-test_1234567890abcdef was returned.",
            needs_manual_review=True,
        )
        self.assertIn("[REDACTED_SECRET]", candidate.evidence_snippet)
        self.assertFalse(contains_unredacted_sensitive_marker(candidate.evidence_snippet))

    def test_recommendation_selection(self) -> None:
        recommendation = recommendation_for_category("tool_function_abuse")
        self.assertIn("permission checks", recommendation)
        self.assertIn("rate limits", recommendation_for_category("cost_abuse"))


class GroupingMergeSortTests(unittest.TestCase):
    def test_duplicate_grouping_and_merge_preserves_strongest_values(self) -> None:
        first = FindingCandidate(
            category="rag_data_leakage",
            detector_name="canary_token_disclosed",
            severity_hint="medium",
            confidence_hint="medium",
            observed_behavior="response contains a restricted demo canary token.",
            redacted_evidence="The marker is [REDACTED_CANARY].",
            test_case_id="SHK-APL-RAG-001",
            affected_target="Demo Support Assistant",
        )
        second = FindingCandidate(
            category="rag_data_leakage",
            detector_name="canary_token_disclosed",
            severity_hint="critical",
            confidence_hint="high",
            observed_behavior="response contains a restricted demo canary token.",
            redacted_evidence="Again returned [REDACTED_CANARY].",
            test_case_id="SHK-APL-RAG-002",
            affected_target="Demo Support Assistant",
            needs_manual_review=True,
        )
        groups = group_duplicate_candidates([first, second])
        self.assertEqual(len(groups), 1)
        merged = merge_candidate_group(next(iter(groups.values())))
        self.assertEqual(merged.severity_hint, "critical")
        self.assertEqual(merged.confidence_hint, "high")
        self.assertEqual(merged.source_test_ids, ["SHK-APL-RAG-001", "SHK-APL-RAG-002"])
        self.assertTrue(merged.metadata["merged"])

    def test_sort_findings_uses_severity_confidence_then_title(self) -> None:
        low = _finding(severity="low", confidence="high")
        critical = _finding(severity="critical", confidence="medium", manual_review_required=True)
        high = _finding(severity="high", confidence="high", strong_evidence=True)
        ordered = sort_findings([low, critical, high])
        self.assertEqual([item.severity for item in ordered], ["critical", "high", "low"])


class EvaluatorAdapterTests(unittest.TestCase):
    def test_evaluator_output_to_candidates_and_findings(self) -> None:
        payload = {
            "source_scan_id": "shk_demo_scan",
            "source_target_name": "Demo RAG Assistant",
            "evaluations": [
                {
                    "test_id": "SHK-APL-RAG-001",
                    "category": "rag_data_leakage",
                    "verdict": "vulnerable",
                    "severity": "critical",
                    "confidence": "high",
                    "matched_signals": [
                        {
                            "name": "canary_token_disclosed",
                            "group": "canary_token_leakage",
                            "severity": "critical",
                            "confidence": "high",
                            "evidence_count": 1,
                            "description": "Response contains a fake/demo canary token associated with the test metadata.",
                        }
                    ],
                    "evidence": [
                        {
                            "signal": "canary_token_leakage",
                            "snippet": "The restricted marker is FAKE-CANARY-NOVA-042.",
                            "redacted_snippet": "The restricted marker is [REDACTED_CANARY].",
                            "start": 25,
                            "end": 47,
                        }
                    ],
                    "reasoning_summary": "Deterministic Phase 7 rules matched one canary signal.",
                    "needs_manual_review": True,
                    "manual_review_reasons": ["high_impact_signal_requires_review"],
                    "evaluator_version": "phase_7_evaluator_v0.1",
                },
                {
                    "test_id": "safe-demo",
                    "category": "prompt_injection",
                    "verdict": "safe",
                    "severity": "none",
                    "confidence": "medium",
                    "matched_signals": [],
                    "evidence": [],
                    "reasoning_summary": "No deterministic signals matched.",
                    "needs_manual_review": False,
                    "manual_review_reasons": [],
                },
            ],
        }
        candidates = candidates_from_evaluator_output(payload)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].source_scan_id, "shk_demo_scan")
        self.assertEqual(candidates[0].category, "rag_data_leakage")
        findings = findings_from_candidates(candidates)
        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding.status, "needs_review")
        self.assertEqual(finding.severity, "critical")
        self.assertTrue(finding.manual_review_required)
        self.assertIn("document-level authorization", finding.fix_recommendation)
        self.assertIn("[REDACTED_CANARY]", finding.evidence_summary)


if __name__ == "__main__":
    unittest.main()
