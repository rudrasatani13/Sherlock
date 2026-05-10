"""CLI for the Phase 19 PDF export foundation."""
from __future__ import annotations

import argparse
import json
from typing import Any

from packages.report_system.cli import _demo_report
from packages.report_system.builder import build_report
from packages.findings_system import EvidenceItem, Finding

from .models import PDF_EXPORT_STATUSES, PDF_EXPORT_SYSTEM_VERSION, PDF_EXPORT_TYPES
from .renderer import render_print_html, write_print_html
from .safety import ALLOWED_OUTPUT_DIRECTORIES
from .template import build_pdf_export_from_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect or render the Sherlock Phase 19 PDF export foundation.")
    parser.add_argument("--demo", action="store_true", help="Print a static demo PDF export object as JSON.")
    parser.add_argument("--render-html", action="store_true", help="Print the print-ready HTML demo export to stdout.")
    parser.add_argument("--write-html", action="store_true", help="Write a local ignored print-ready HTML demo artifact.")
    parser.add_argument("--output-dir", default="pdf-exports", help="Relative output directory for --write-html.")
    args = parser.parse_args()

    export = build_pdf_export_from_report(_demo_report_object(), generated_at="2026-05-10T00:00:00Z")
    if args.write_html:
        target = write_print_html(export, args.output_dir)
        print(json.dumps({"written": str(target), "filename": export.filename}, indent=2, sort_keys=True))
        return
    if args.render_html:
        print(render_print_html(export))
        return
    if args.demo:
        print(json.dumps(export.to_dict(), indent=2, sort_keys=True))
        return
    print(json.dumps(_schema(), indent=2, sort_keys=True))


def _schema() -> dict[str, Any]:
    return {
        "package": "packages.pdf_export",
        "version": PDF_EXPORT_SYSTEM_VERSION,
        "export_statuses": list(PDF_EXPORT_STATUSES),
        "export_types": list(PDF_EXPORT_TYPES),
        "default_output_directories": list(ALLOWED_OUTPUT_DIRECTORIES),
        "current_behavior": "PDF export contract, safety checks, print-ready HTML renderer, and local/demo CLI only.",
        "disabled_capabilities": [
            "production PDF export for real customer reports",
            "public PDF download links",
            "public report sharing",
            "billing or Stripe",
            "paid-plan enforcement",
            "active report database persistence",
            "production storage integration",
            "real customer evidence storage",
            "Phase 20 retest flow",
        ],
    }


def _demo_report_object():
    finding = Finding(
        finding_id="SHK-DEMO-PDF-001",
        title="RAG data leakage demo canary disclosure",
        category="rag_data_leakage",
        severity="high",
        confidence="high",
        status="needs_review",
        description="The demo assistant returned a redacted canary marker from a restricted fictional document.",
        business_impact="Restricted retrieved content may be exposed outside the intended authorization boundary.",
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
        reproduction_steps=["Run the approved demo RAG leakage test case inside the documented scope."],
        fix_recommendation="Add document-level authorization and retrieval filtering before model context assembly.",
        manual_review_required=True,
    )
    return build_report(
        metadata={
            "report_id": "SHK-DEMO-PDF-REPORT",
            "title": "AI Launch Security Report",
            "project_name": "Demo Project",
            "target_name": "NovaDesk AI Support Copilot",
            "scan_type": "static_demo",
            "generated_at": "2026-05-09T00:00:00Z",
        },
        findings=[finding],
        tested_categories=["rag_data_leakage", "prompt_injection"],
        not_tested=["real customer integrations", "production tool execution"],
    )


if __name__ == "__main__":
    main()
