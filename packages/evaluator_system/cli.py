from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .constants import EVALUATOR_VERSION
from .evaluator import evaluate_scan_result
from .models import utc_now_iso

DEFAULT_OUTPUT_DIR = "scan-results/evaluations"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a Sherlock scanner result file locally.")
    parser.add_argument("--input", required=True, help="Path to a Phase 5 scan-result.json or single test-result JSON file.")
    parser.add_argument("--output", help="Optional output JSON path. Defaults to scan-results/evaluations/.")
    parser.add_argument("--stdout", action="store_true", help="Print the full evaluation JSON instead of writing a file.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing output file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    payload = _read_json(input_path)
    evaluation = evaluate_scan_result(payload)

    if args.stdout:
        print(json.dumps(evaluation, indent=2, sort_keys=True))
        return

    output_path = Path(args.output) if args.output else _default_output_path(input_path, evaluation)
    _write_json(output_path, evaluation, overwrite=args.overwrite)
    summary = {
        "evaluator_version": EVALUATOR_VERSION,
        "evaluated_at": utc_now_iso(),
        "input_path": str(input_path),
        "output_path": str(output_path),
        "summary": evaluation["summary"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError("input JSON root must be an object")
    return payload


def _write_json(path: Path, payload: Dict[str, Any], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"output file already exists: {path}. Pass --overwrite or choose a new --output path.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)
        file.write("\n")


def _default_output_path(input_path: Path, evaluation: Dict[str, Any]) -> Path:
    scan_id = evaluation.get("source_scan_id") or input_path.stem
    safe_scan_id = "".join(character if character.isalnum() or character in {"-", "_"} else "_" for character in str(scan_id))
    return Path(DEFAULT_OUTPUT_DIR) / f"{safe_scan_id}-evaluation.json"


if __name__ == "__main__":
    main()
