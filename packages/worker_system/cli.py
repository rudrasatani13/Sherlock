"""Local worker CLI for Sherlock — Phase 15 foundation.

This CLI can:
- Load a demo/mock job payload
- Validate the job payload against safety gates
- Run a safe mock scan using the Phase 5 scanner MockTargetAdapter only
- Write local worker output to an ignored output folder
- NOT scan external targets
- NOT require real Redis, Supabase, or real secrets
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .jobs import JobPayload, JobType, create_job_payload
from .queue import LocalMemoryQueue
from .safety import check_safety_gates
from .worker import WorkerConfig, WorkerEngine, write_worker_result


DEFAULT_OUTPUT_DIR = "worker-output"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the local Sherlock worker for Phase 15 foundation dry-runs.",
    )
    parser.add_argument(
        "--job",
        help="Path to a job payload JSON file. If omitted, a demo mock job is generated.",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for worker results (default: {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate the job payload against safety gates, do not execute.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the result JSON to stdout instead of writing a file.",
    )
    return parser


def _load_or_create_payload(job_path: str | None) -> JobPayload:
    """Load a job payload from a file or create a demo mock payload."""
    if job_path:
        path = Path(job_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Job payload JSON root must be an object.")
        return JobPayload.from_dict(data)

    # Generate a safe demo mock payload
    return create_job_payload(
        JobType.SCAN_RUN,
        scan_type="safe_smoke",
        verification_status="verified",
        target_snapshot={
            "name": "Worker Demo Mock Target",
            "type": "mock",
            "notes": "Phase 15 local worker dry-run — no network requests",
        },
        limits={"max_tests": 3, "timeout_seconds": 10},
        metadata={
            "source": "phase_15_local_cli",
            "dry_run": True,
        },
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        payload = _load_or_create_payload(args.job)
    except Exception as error:
        print(f"Failed to load job payload: {error}", file=sys.stderr)
        return 1

    print(f"Job ID:   {payload.job_id}")
    print(f"Job Type: {payload.job_type}")
    print(f"Scan Type: {payload.scan_type}")
    print(f"Verification: {payload.verification_status}")
    print()

    # Validate safety gates (skip queue_enabled for local dry-runs)
    gate_result = check_safety_gates(payload, skip_queue_enabled_check=True)
    print("Safety gates:")
    for gate in gate_result.gate_results:
        status = "PASS" if gate["passed"] else "FAIL"
        reason = f" — {gate['reason']}" if gate.get("reason") else ""
        print(f"  [{status}] {gate['gate']}{reason}")
    print()

    if not gate_result.passed:
        print(f"BLOCKED: {gate_result.blocked_reason}", file=sys.stderr)
        return 1

    if args.validate_only:
        print("Validation passed. Skipping execution (--validate-only).")
        return 0

    # Execute via worker engine
    config = WorkerConfig(output_dir=args.output_dir, dry_run=True)
    queue = LocalMemoryQueue()
    engine = WorkerEngine(queue=queue, config=config)
    result = engine.execute(payload)

    print(f"Status: {result.status}")
    print(f"Duration: {result.duration_ms}ms")
    if result.error_message:
        print(f"Error: {result.error_message}", file=sys.stderr)

    if args.stdout:
        print()
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        output_path = write_worker_result(result, args.output_dir)
        print(f"Result written to: {output_path}")

    return 0 if result.status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
