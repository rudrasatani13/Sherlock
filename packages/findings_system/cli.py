"""Local CLI for converting safe evaluator output into Phase 17 findings."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from . import FINDINGS_SYSTEM_VERSION
from .normalizer import candidates_from_evaluator_output, findings_from_candidates


def build_findings_payload(evaluator_payload: Dict[str, Any]) -> Dict[str, Any]:
    candidates = candidates_from_evaluator_output(evaluator_payload)
    findings = findings_from_candidates(candidates)
    return {
        "findings_system_version": FINDINGS_SYSTEM_VERSION,
        "phase": "Phase 17 Findings System foundation",
        "source_scan_id": evaluator_payload.get("source_scan_id"),
        "source_target_name": evaluator_payload.get("source_target_name"),
        "candidate_count": len(candidates),
        "finding_count": len(findings),
        "findings": [finding.to_dict() for finding in findings],
        "notes": [
            "Local conversion only; no database writes are performed.",
            "Evidence is redacted and summarized for report review.",
            "This does not generate a Phase 18 web report or PDF.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Phase 7 evaluator output into Phase 17 finding objects.")
    parser.add_argument("--input", required=True, help="Path to evaluator JSON output.")
    parser.add_argument("--output", help="Optional output path. Defaults to stdout to avoid committed artifacts.")
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open("r", encoding="utf-8") as handle:
        evaluator_payload = json.load(handle)
    payload = build_findings_payload(evaluator_payload)

    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f"{rendered}\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
