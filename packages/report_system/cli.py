"""CLI helpers for the Phase 18 report system.

The CLI prints schema/demo metadata to stdout only. It does not read scan
outputs by default and does not write generated report files.
"""
from __future__ import annotations

import argparse
import json
from typing import Any

from packages.findings_system import EvidenceItem, Finding

from .builder import build_report
from .models import LAUNCH_READINESS_VERDICTS, REPORT_STATUSES, REPORT_TYPES, REPORT_SYSTEM_VERSION
from .sections import DEFAULT_LIMITATIONS


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect the Sherlock Phase 18 report system contract.")
    parser.add_argument("--demo", action="store_true", help="Print a static demo report object to stdout.")
    args = parser.parse_args()
    payload = _demo_report() if args.demo else _schema()
    print(json.dumps(payload, indent=2, sort_keys=True))


def _schema() -> dict[str, Any]:
    return {
        "package": "packages.report_system",
        "version": REPORT_SYSTEM_VERSION,
        "report_statuses": list(REPORT_STATUSES),
        "report_types": list(REPORT_TYPES),
        "launch_readiness_verdicts": list(LAUNCH_READINESS_VERDICTS),
        "default_limitations": list(DEFAULT_LIMITATIONS),
        "current_behavior": "Schema and builder helpers only. No PDF export, persistence, sharing tokens, or scan execution.",
    }


def _demo_report() -> dict[str, Any]:
    finding = Finding(
        finding_id="SHK-DEMO-WEB-001",
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
        reproduction_steps=["Run the approved demo RAG leakage test case."],
        fix_recommendation="Add document-level authorization and retrieval filtering before model context assembly.",
        manual_review_required=True,
    )
    report = build_report(
        metadata={
            "report_id": "SHK-DEMO-WEB-REPORT",
            "title": "AI Launch Security Web Report",
            "project_name": "Demo Project",
            "target_name": "NovaDesk AI Support Copilot",
            "scan_type": "static_demo",
            "generated_at": "2026-05-09T00:00:00Z",
        },
        findings=[finding],
        tested_categories=["rag_data_leakage", "prompt_injection"],
        not_tested=["real customer integrations", "production tool execution"],
    )
    return report.to_dict()


if __name__ == "__main__":
    main()
