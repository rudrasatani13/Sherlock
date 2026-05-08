"""Scan limit integration for worker system safety gates.

Phase 16 adds a scan_type_limits gate that validates job payloads against
the scan type limit definitions in packages/scan_limits. This integrates
with the existing Phase 15 safety gate pipeline.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from packages.scan_limits.scan_types import get_scan_type, ScanType
from packages.scan_limits.validators import validate_scan_request


def check_scan_type_limits(payload_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a worker job payload against Phase 16 scan type limits.

    Returns a gate result dict compatible with Phase 15 safety gate format:
    {"gate": str, "passed": bool, "reason": str}
    """
    scan_type = payload_dict.get("scan_type", "")
    verification_status = payload_dict.get("verification_status", "unverified")
    limits = payload_dict.get("limits", {})
    metadata = payload_dict.get("metadata", {})

    # Extract requested values from payload
    requested_max_tests = limits.get("max_tests")
    requested_timeout = limits.get("timeout_seconds")
    requested_concurrency = limits.get("max_concurrency")
    requested_categories = metadata.get("requested_categories")
    manual_review_flag = metadata.get("manual_review_flag", False)
    manual_authorization_override = metadata.get("manual_authorization_override", False)

    # Build payload for secret check (target_snapshot + metadata)
    check_payload: Dict[str, Any] = {}
    if payload_dict.get("target_snapshot"):
        check_payload.update(payload_dict["target_snapshot"])
    if metadata:
        check_payload.update(metadata)

    # Skip validation for legacy safe_smoke type (Phase 5/15 mock scans)
    if scan_type == "safe_smoke":
        return {
            "gate": "scan_type_limits",
            "passed": True,
            "reason": "Legacy safe_smoke scan type — Phase 15 mock only.",
        }

    # Validate against scan type limits
    result = validate_scan_request(
        scan_type,
        verification_status=verification_status,
        requested_categories=requested_categories,
        requested_max_tests=requested_max_tests,
        requested_timeout=requested_timeout,
        requested_concurrency=requested_concurrency,
        manual_review_flag=manual_review_flag,
        manual_authorization_override=manual_authorization_override,
        payload=check_payload if check_payload else None,
    )

    if result.valid:
        return {
            "gate": "scan_type_limits",
            "passed": True,
            "reason": "",
        }
    else:
        return {
            "gate": "scan_type_limits",
            "passed": False,
            "reason": f"Scan limit validation failed: {'; '.join(result.errors)}",
        }
