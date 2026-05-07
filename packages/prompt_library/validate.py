from __future__ import annotations

import json
import sys
from collections import Counter

from .loader import load_prompt_library, validate_prompt_library


def main() -> int:
    errors = validate_prompt_library()
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2, sort_keys=True), file=sys.stderr)
        return 1
    library = load_prompt_library()
    counts = Counter(test_case.category for test_case in library.test_cases)
    print(
        json.dumps(
            {
                "valid": True,
                "library_version": library.manifest.get("version"),
                "total_test_cases": len(library.test_cases),
                "enabled_test_cases": len(library.enabled_cases()),
                "categories": dict(sorted(counts.items())),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
