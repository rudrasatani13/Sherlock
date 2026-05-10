from __future__ import annotations

import unittest

from packages.findings_system import EvidenceItem, Finding, candidates_from_evaluator_output, findings_from_candidates
from packages.report_system import (
    Report,
    build_limitations,
    build_report,
    build_severity_breakdown,
    calculate_security_score,
    format_tested_categories,
    redacted_report_evidence_summary,
    select_launch_readiness_verdict,
    select_top_fixes,
    shape_findings_table,
)
from packages.report_system.evidence import format_report_evidence_items
from packages.report_system.models import (
    LaunchReadinessVerdict,
    SecurityScore,
    VERDICT_HIGH_RISK_DO_NOT_LAUNCH,
    VERDICT_MANUAL_REVIEW_REQUIRED,
    VERDICT_NEEDS_FIXES_BEFORE_LAUNCH,
    VERDICT_READY_WITH_LOW_RISK,
)


def _finding(
    *,
    finding_id: str = "SHK-DEMO-001",
    title: str = "RAG data leakage demo canary disclosure",
    category: str = "rag_data_leakage",
    severity: str = "high",
    confidence: str = "high",
    status: str = "open",
    recommendation: str = "Add document-level authorization and retrieval filters before model context assembly.",
    business_impact: str = "Customer tenant documents may be exposed outside the intended authorization boundary.",
    manual_review_required: bool = False,
) -> Finding:
    return Finding(
        finding_id=finding_id,
        title=title,
        category=category,
        severity=severity,
        confidence=confidence,
        status=status,
        description="The demo assistant returned restricted fictional content during an approved test.",
        business_impact=business_impact,
        evidence_summary="The response contained [REDACTED_CANARY].",
        evidence_items=[
            EvidenceItem(
                signal="canary_token_leakage",
                summary="The response contained [REDACTED_CANARY].",
                redacted_snippet="The response contained [REDACTED_CANARY].",
                source_test_id="SHK-APL-RAG-001",
                strong_evidence=True,
            )
        ],
        reproduction_steps=["Run the approved test case inside the documented scope."],
        fix_recommendation=recommendation,
        source_scan_id="shk_demo_scan",
        source_test_ids=["SHK-APL-RAG-001"],
        manual_review_required=manual_review_required,
    )


class ReportModelTests(unittest.TestCase):
    def test_report_model_validation_and_serialization(self) -> None:
        report = build_report(
            metadata={
                "report_id": "SHK-REPORT-DEMO",
                "report_type": "web",
                "project_name": "Demo Project",
                "target_name": "NovaDesk AI Support Copilot",
                "scan_type": "standard_scan",
                "generated_at": "2026-05-09T00:00:00Z",
            },
            findings=[_finding()],
            tested_categories=["rag_data_leakage", "prompt_injection"],
            not_tested=["production tool execution"],
        )
        self.assertIsInstance(report, Report)
        data = report.to_dict()
        self.assertEqual(data["report_id"], "SHK-REPORT-DEMO")
        self.assertEqual(data["report_status"], "draft")
        self.assertEqual(data["report_type"], "web")
        self.assertIn("launch_readiness_verdict", data)
        self.assertIn("security_score", data)
        self.assertIn("limitations", data)

    def test_invalid_status_type_and_overclaiming_verdict_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_report(metadata={"report_status": "published"}, tested_categories=["prompt_injection"])
        with self.assertRaises(ValueError):
            build_report(metadata={"report_type": "pdf"}, tested_categories=["prompt_injection"])
        with self.assertRaises(ValueError):
            LaunchReadinessVerdict(
                verdict=VERDICT_READY_WITH_LOW_RISK,
                label="Certified secure",
                summary="No risk exists.",
                recommended_action="Launch.",
            )


class ScoreVerdictTests(unittest.TestCase):
    def test_score_calculation_is_bounded_and_conservative(self) -> None:
        score = calculate_security_score([
            _finding(severity="critical", confidence="high", manual_review_required=True),
            _finding(finding_id="SHK-DEMO-LOW", severity="low", confidence="low"),
        ])
        self.assertGreaterEqual(score.score, 0)
        self.assertLessEqual(score.score, 44)
        self.assertIn("No findings observed does not automatically mean a 100 score.", score.limitations)

    def test_no_findings_does_not_score_100(self) -> None:
        score = calculate_security_score([])
        self.assertEqual(score.score, 88)
        self.assertLess(score.score, 100)

    def test_needs_review_caps_score(self) -> None:
        score = calculate_security_score([
            _finding(status="needs_review", severity="medium", confidence="medium", manual_review_required=True)
        ])
        self.assertLessEqual(score.score, 76)

    def test_launch_readiness_verdict_selection(self) -> None:
        tested = format_tested_categories(["prompt_injection", "rag_data_leakage"])
        critical_score = SecurityScore(score=40)
        critical = select_launch_readiness_verdict([_finding(severity="critical", manual_review_required=True)], critical_score, tested_categories=tested)
        self.assertEqual(critical.verdict, VERDICT_HIGH_RISK_DO_NOT_LAUNCH)

        high = select_launch_readiness_verdict([_finding(severity="high")], SecurityScore(score=68), tested_categories=tested)
        self.assertEqual(high.verdict, VERDICT_NEEDS_FIXES_BEFORE_LAUNCH)

        review = select_launch_readiness_verdict(
            [_finding(severity="low", status="needs_review", manual_review_required=True)],
            SecurityScore(score=76),
            tested_categories=tested,
        )
        self.assertEqual(review.verdict, VERDICT_MANUAL_REVIEW_REQUIRED)

        ready = select_launch_readiness_verdict(
            [_finding(severity="low", status="fixed")],
            SecurityScore(score=88),
            tested_categories=tested,
        )
        self.assertEqual(ready.verdict, VERDICT_READY_WITH_LOW_RISK)


class SectionBuilderTests(unittest.TestCase):
    def test_severity_breakdown_counts_findings(self) -> None:
        breakdown = build_severity_breakdown([
            _finding(severity="critical", manual_review_required=True),
            _finding(finding_id="SHK-DEMO-HIGH", severity="high"),
            _finding(finding_id="SHK-DEMO-INFO", severity="informational", confidence="low"),
        ])
        self.assertEqual(breakdown.critical, 1)
        self.assertEqual(breakdown.high, 1)
        self.assertEqual(breakdown.informational, 1)
        self.assertEqual(breakdown.total, 3)

    def test_top_fixes_sort_and_deduplicate(self) -> None:
        shared_fix = "Add document-level authorization and retrieval filters before model context assembly."
        fixes = select_top_fixes([
            _finding(finding_id="A", severity="medium", confidence="high", recommendation=shared_fix),
            _finding(finding_id="B", severity="critical", confidence="medium", recommendation=shared_fix, manual_review_required=True),
            _finding(
                finding_id="C",
                category="tool_function_abuse",
                severity="high",
                confidence="high",
                recommendation="Add tool allowlists, server-side permission checks, argument validation, and human confirmation.",
            ),
        ])
        self.assertEqual(len(fixes), 2)
        self.assertEqual(fixes[0].severity, "critical")
        self.assertEqual(fixes[0].finding_ids, ["A", "B"])

    def test_findings_table_data_shape(self) -> None:
        rows = shape_findings_table([_finding()])
        self.assertEqual(rows[0]["title"], "RAG data leakage demo canary disclosure")
        self.assertEqual(rows[0]["category"], "rag_data_leakage")
        self.assertEqual(rows[0]["severity"], "high")
        self.assertIn("Customer tenant", rows[0]["business_impact_summary"])
        self.assertIn("document-level", rows[0]["fix_recommendation_summary"])

    def test_tested_categories_formatting_and_limitations(self) -> None:
        categories = format_tested_categories([
            "prompt_injection",
            {"category": "cost_abuse", "notes": "Bounded retry behavior reviewed."},
            "prompt_injection",
        ])
        self.assertEqual([item.category for item in categories], ["prompt_injection", "cost_abuse_unbounded_consumption"])
        limitations = build_limitations(["Demo-only reviewer note."])
        self.assertTrue(any("not a guarantee of security" in item for item in limitations))
        self.assertTrue(any("sanitized static demo" in item for item in limitations))
        self.assertIn("Demo-only reviewer note.", limitations)


class EvidenceBuilderIntegrationTests(unittest.TestCase):
    def test_report_safe_evidence_redacts_headers_cookies_keys_and_private_documents(self) -> None:
        raw = (
            "Authorization: Bearer abcdef1234567890\n"
            "Cookie: sid=secret-value;\n"
            "<private_document>full private document</private_document>\n"
            "api_key=sk-test_1234567890abcdef"
        )
        redacted = redacted_report_evidence_summary(raw)
        self.assertIn("[REDACTED_HEADER]", redacted)
        self.assertIn("[REDACTED_COOKIE]", redacted)
        self.assertIn("[REDACTED_PRIVATE_DOCUMENT]", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)
        self.assertLessEqual(len(redacted), 240)

    def test_evidence_items_reject_unredacted_sensitive_markers_after_formatting(self) -> None:
        items = format_report_evidence_items([
            {
                "signal": "assigned_secret",
                "summary": "The api_key=sk-test_1234567890abcdef was returned.",
                "redacted_snippet": "",
                "source_test_id": "SHK-APL-SDL-001",
            }
        ])
        self.assertIn("[REDACTED_SECRET]", items[0].summary)

    def test_builder_accepts_phase17_finding_objects_from_evaluator_candidates(self) -> None:
        payload = {
            "source_scan_id": "shk_demo_scan",
            "source_target_name": "Demo RAG Assistant",
            "evaluations": [
                {
                    "test_id": "SHK-APL-RAG-001",
                    "category": "rag_data_leakage",
                    "verdict": "vulnerable",
                    "severity": "high",
                    "confidence": "high",
                    "matched_signals": [
                        {
                            "name": "canary_token_disclosed",
                            "group": "canary_token_leakage",
                            "severity": "high",
                            "confidence": "high",
                            "description": "Response contains a fake/demo canary token associated with the test metadata.",
                        }
                    ],
                    "evidence": [
                        {
                            "signal": "canary_token_leakage",
                            "snippet": "The restricted marker is FAKE-CANARY-NOVA-042.",
                            "redacted_snippet": "The restricted marker is [REDACTED_CANARY].",
                        }
                    ],
                    "reasoning_summary": "Deterministic Phase 7 rules matched one canary signal.",
                    "needs_manual_review": True,
                    "manual_review_reasons": ["high_impact_signal_requires_review"],
                }
            ],
        }
        findings = findings_from_candidates(candidates_from_evaluator_output(payload))
        report = build_report(
            metadata={"project_name": "Demo Project", "target_name": "Demo RAG Assistant"},
            findings=findings,
            tested_categories=["rag_data_leakage"],
            not_tested=["production integrations"],
        )
        self.assertEqual(report.findings[0].category, "rag_data_leakage")
        self.assertEqual(report.findings[0].status, "needs_review")
        self.assertIn("[REDACTED_CANARY]", report.findings[0].evidence_summary)
        self.assertEqual(report.source_scan_id, "shk_demo_scan")


if __name__ == "__main__":
    unittest.main()
