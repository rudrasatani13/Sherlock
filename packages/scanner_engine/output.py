from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .models import ScanRun


OUTPUT_FILENAMES = {
    "raw_results": "raw-results.json",
    "structured_result": "scan-result.json",
    "summary": "summary.json",
}


def write_scan_outputs(scan_run: ScanRun, output_dir: str) -> Dict[str, str]:
    run_dir = Path(output_dir) / scan_run.session.scan_id
    run_dir.mkdir(parents=True, exist_ok=False)
    paths = {
        "raw_results": str(run_dir / OUTPUT_FILENAMES["raw_results"]),
        "structured_result": str(run_dir / OUTPUT_FILENAMES["structured_result"]),
        "summary": str(run_dir / OUTPUT_FILENAMES["summary"]),
    }
    _write_json(paths["raw_results"], scan_run.to_raw_results())
    _write_json(paths["structured_result"], scan_run.to_structured_result())
    scan_run.output_paths = paths
    _write_json(paths["summary"], scan_run.to_summary())
    return paths


def _write_json(path: str, payload: Dict[str, Any]) -> None:
    with Path(path).open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)
        file.write("\n")
