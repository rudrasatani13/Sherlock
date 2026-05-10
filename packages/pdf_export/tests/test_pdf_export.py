from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from packages.findings_system import EvidenceItem, Finding
from packages.pdf_export import (
    PDF_EXPORT_STATUSES,
    PdfReportExport,
    build_pdf_export_from_report,
    normalize_export_status,
    render_print_html,
    resolve_export_path,
    safe_report_filename,
    validate_pdf_evidence_text,
    validate_pdf_export_safety,
    write_print_html,
)
from packages.pdf_export.cli import _schema
from packages.report_system import build_report


def _finding(evidence: str = "The response contained [REDACTED_CANARY].") -> Finding:
    return Finding(
        finding_id="SHK-DEMO-PDF-001",
        title="RAG data leakage demo canary disclosure",
        category="rag_data_leakage",
        severity="high",
        confidence="high",
        status="needs_review",
        description="The demo assistant returned a redacted canary marker from a restricted fictional document.",
        business_impact="Restricted retrieved content may be exposed outside the intended authorization boundary.",
        evidence_summary=evidence,
        evidence_items=[
            EvidenceItem(
                signal="canary_token_leakage",
                summary=evidence,
                redacted_snippet=evidence,
                source_test_id="SHK-APL-RAG-001",
                strong_evidence=True,
            )
        ],
        reproduction_steps=["Run the approved demo RAG leakage test case inside the documented scope."],
        fix_recommendation="Add document-level authorization and retrieval filtering before model context assembly.",
        manual_review_required=True,
    )


def _report():
    return build_report(
        metadata={
            "report_id": "SHK-DEMO-PDF-REPORT",
            "title": "AI Launch Security Report",
            "project_name": "Demo Project",
            "target_name": "NovaDesk AI Support Copilot",
            "scan_type": "static_demo",
            "generated_at": "2026-05-09T00:00:00Z",
        },
        findings=[_finding()],
        tested_categories=["rag_data_leakage", "prompt_injection"],
        not_tested=["real customer integrations", "production tool execution"],
    )


class PdfExportModelTests(unittest.TestCase):
    def test_export_model_statuses_and_serialization(self) -> None:
        export = build_pdf_export_from_report(_report(), generated_at="2026-05-10T00:00:00Z")
        self.assertIsInstance(export, PdfReportExport)
        self.assertEqual(export.export_status, "draft")
        self.assertEqual(export.export_type, "print_html")
        self.assertIn("blocked_sensitive_evidence", PDF_EXPORT_STATUSES)
        self.assertEqual(normalize_export_status("blocked sensitive evidence"), "blocked_sensitive_evidence")
        data = export.to_dict()
        self.assertEqual(data["report_id"], "SHK-DEMO-PDF-REPORT")
        self.assertIn("cover_page", data)
        self.assertIn("findings_table", data)
        self.assertIn("detailed_findings", data)
        self.assertIn("limitations", data)

    def test_invalid_export_status_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_export_status("published")

    def test_safe_filename_generation(self) -> None:
        self.assertEqual(
            safe_report_filename("SHK Report/../Demo", "pdf"),
            "powerdetect-sherlock-report-shk-report-demo.pdf",
        )
        self.assertEqual(
            safe_report_filename("SHK-DEMO-PDF-REPORT"),
            "powerdetect-sherlock-report-shk-demo-pdf-report.html",
        )


class PdfExportSafetyTests(unittest.TestCase):
    def test_evidence_safety_rejects_raw_sensitive_markers(self) -> None:
        with self.assertRaises(ValueError):
            validate_pdf_evidence_text("Authorization: Bearer abcdef1234567890")
        with self.assertRaises(ValueError):
            validate_pdf_evidence_text("Cookie: sid=secret")
        with self.assertRaises(ValueError):
            validate_pdf_evidence_text("-----BEGIN PRIVATE KEY-----")
        with self.assertRaises(ValueError):
            validate_pdf_evidence_text("<private_document>full text</private_document>")

    def test_overclaiming_verdict_is_rejected(self) -> None:
        export = build_pdf_export_from_report(_report(), generated_at="2026-05-10T00:00:00Z")
        export.verdict["summary"] = "No risk exists and all vulnerabilities were found."
        with self.assertRaises(ValueError):
            validate_pdf_export_safety(export)

    def test_limitations_are_required(self) -> None:
        export = build_pdf_export_from_report(_report(), generated_at="2026-05-10T00:00:00Z")
        export.limitations = []
        with self.assertRaises(ValueError):
            validate_pdf_export_safety(export)

    def test_path_traversal_and_output_directory_rules(self) -> None:
        with self.assertRaises(ValueError):
            resolve_export_path("../tmp", "powerdetect-sherlock-report-demo.html")
        with self.assertRaises(ValueError):
            resolve_export_path("tmp", "powerdetect-sherlock-report-demo.html")
        with self.assertRaises(ValueError):
            resolve_export_path("pdf-exports", "../powerdetect-sherlock-report-demo.html")
        target = resolve_export_path("pdf-exports", "powerdetect-sherlock-report-demo.html", base_dir="/tmp/sherlock")
        self.assertEqual(
            target,
            Path("/tmp/sherlock/pdf-exports/powerdetect-sherlock-report-demo.html").resolve(),
        )


class PdfExportTemplateRendererTests(unittest.TestCase):
    def test_template_sections_are_generated_from_phase18_report(self) -> None:
        export = build_pdf_export_from_report(_report(), generated_at="2026-05-10T00:00:00Z")
        self.assertEqual(export.cover_page.brand, "PowerDetect")
        self.assertEqual(export.cover_page.product_name, "Sherlock")
        self.assertEqual(len(export.findings_table), 1)
        self.assertEqual(len(export.detailed_findings), 1)
        self.assertIn("RAG data leakage", export.findings_table[0].category)
        self.assertIn("[REDACTED_CANARY]", export.detailed_findings[0].evidence_snippets[0])

    def test_print_html_renderer_contains_required_sections(self) -> None:
        export = build_pdf_export_from_report(_report(), generated_at="2026-05-10T00:00:00Z")
        html = render_print_html(export)
        self.assertIn("Executive summary", html)
        self.assertIn("Verdict and score", html)
        self.assertIn("Findings table", html)
        self.assertIn("Detailed findings", html)
        self.assertIn("Limitations and evidence handling", html)
        self.assertIn("Phase 20 retest flow is not implemented", html)

    def test_cli_schema_is_dry_run_and_documents_disabled_capabilities(self) -> None:
        schema = _schema()
        self.assertEqual(schema["package"], "packages.pdf_export")
        self.assertIn("print_html", schema["export_types"])
        self.assertIn("production PDF export for real customer reports", schema["disabled_capabilities"])

    def test_write_print_html_stays_inside_allowed_output_directory(self) -> None:
        export = build_pdf_export_from_report(_report(), generated_at="2026-05-10T00:00:00Z")
        with tempfile.TemporaryDirectory() as temp_dir:
            target = write_print_html(export, "pdf-exports/demo", base_dir=temp_dir)
            self.assertTrue(target.exists())
            self.assertTrue(str(target).startswith(str(Path(temp_dir).resolve() / "pdf-exports")))
            self.assertIn("PowerDetect Sherlock", target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
