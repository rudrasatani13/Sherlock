from __future__ import annotations

import argparse
import json
import sys

from .config import load_scan_config
from .runner import ScannerEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the internal PowerDetect Sherlock scanner engine V0.")
    parser.add_argument("--config", required=True, help="Path to an internal scan config JSON file.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        scan_config = load_scan_config(args.config)
        scan_run = ScannerEngine(scan_config).run()
    except Exception as error:
        print(f"Scanner failed before output creation: {error}", file=sys.stderr)
        return 1
    print(json.dumps(scan_run.to_summary(), indent=2, sort_keys=True))
    return 0 if scan_run.session.state == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
