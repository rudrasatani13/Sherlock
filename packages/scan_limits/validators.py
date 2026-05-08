"""Scan limit validation helpers for Sherlock.

Validates scan requests against defined scan type limits, category rules,
verification requirements, and payload safety. These validators are designed
to be composable and safe for integration with the Phase 15 worker safety
gates.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from .categories import ALL_CATEGORIES, get_categories_for_scan_type
from .scan_types import SCAN_TYPES, ScanType, ScanTypeConfig, get_scan_type

# Re-use the secret detection from worker system if available
try:
    from packages.worker_system.jobs import contains_secret_looking_fields
except ImportError:
    # Standalone fallback — minimal secret field detection
    import re as _re
    _SECRET_REGEX = _re.compile(
        r"(?i)(api_key|api_secret|bearer_token|access_token|refresh_token|"
        r"password|passwd|private_key|secret_key|cookie|session_token|"
        r"x_api_key|authorization_header|raw_header|credential)"
    )

    def contains_secret_looking_fields(data: Dict[str, Any], path: str = "") -> List[str]:
        flagged: List[str] = []
        for key, value in data.items():
            full_path = f"{path}.{key}" if path else key
            if _SECRET_REGEX.search(key):
                flagged.append(full_path)
            if isinstance(value, dict):
                flagged.extend(contains_secret_looking_fields(value, full_path))
        return flagged


# ---------------------------------------------------------------------------
# Validation result
# ---------------------------------------------------------------------------

@dataclass
class ScanLimitValidationResult:
    """Aggregated validation result for a scan request."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    resolved_scan_type: Optional[str] = None
    resolved_config: Optional[ScanTypeConfig] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }
        if self.resolved_scan_type:
            result["resolved_scan_type"] = self.resolved_scan_type
        return result


# ---------------------------------------------------------------------------
# Individual validators
# ---------------------------------------------------------------------------

def validate_scan_type_exists(scan_type: str) -> Optional[str]:
    """Return error message if scan type does not exist, else None."""
    if scan_type not in SCAN_TYPES:
        return f"Unknown scan type '{scan_type}'. Valid types: {sorted(SCAN_TYPES.keys())}"
    return None


def validate_scan_type_enabled(scan_type: str) -> Optional[str]:
    """Return error message if scan type exists but is disabled, else None."""
    config = SCAN_TYPES.get(scan_type)
    if config is None:
        return f"Unknown scan type '{scan_type}'."
    if not config.enabled:
        return f"Scan type '{scan_type}' ({config.display_name}) is currently disabled. It will be available in a future phase."
    return None


def validate_target_verified(
    scan_type: str,
    verification_status: str,
    *,
    manual_authorization_override: bool = False,
) -> Optional[str]:
    """Return error message if target verification is required but missing."""
    config = SCAN_TYPES.get(scan_type)
    if config is None:
        return f"Unknown scan type '{scan_type}'."
    if not config.requires_verified_target:
        return None
    # Manual audit may accept authorization override
    if scan_type == ScanType.MANUAL_AUDIT_ASSISTED and manual_authorization_override:
        return None
    if verification_status != "verified":
        return (
            f"Scan type '{scan_type}' requires a verified target. "
            f"Current status: '{verification_status}'. Complete target ownership verification first."
        )
    return None


def validate_categories_allowed(
    scan_type: str,
    requested_categories: List[str],
) -> Optional[str]:
    """Return error message if any requested category is not allowed for this scan type."""
    config = SCAN_TYPES.get(scan_type)
    if config is None:
        return f"Unknown scan type '{scan_type}'."

    if not requested_categories:
        return None  # No categories requested — use defaults

    requested = set(requested_categories)
    unknown = requested - ALL_CATEGORIES
    if unknown:
        return f"Unknown categories: {sorted(unknown)}. Valid categories: {sorted(ALL_CATEGORIES)}"

    disallowed = requested & config.excluded_categories
    if disallowed:
        return (
            f"Categories {sorted(disallowed)} are not included in scan type '{scan_type}'. "
            f"Allowed categories: {sorted(config.included_categories)}"
        )
    return None


def validate_max_tests(scan_type: str, requested_max_tests: int) -> Optional[str]:
    """Return error message if requested max_tests exceeds scan type limit."""
    config = SCAN_TYPES.get(scan_type)
    if config is None:
        return f"Unknown scan type '{scan_type}'."
    if not isinstance(requested_max_tests, int) or requested_max_tests < 1:
        return "max_tests must be a positive integer."
    if requested_max_tests > config.max_tests:
        return (
            f"Requested max_tests ({requested_max_tests}) exceeds limit "
            f"({config.max_tests}) for scan type '{scan_type}'."
        )
    return None


def validate_timeout(scan_type: str, requested_timeout: int) -> Optional[str]:
    """Return error message if requested timeout exceeds scan type limit."""
    config = SCAN_TYPES.get(scan_type)
    if config is None:
        return f"Unknown scan type '{scan_type}'."
    if not isinstance(requested_timeout, int) or requested_timeout < 1:
        return "timeout_seconds must be a positive integer."
    if requested_timeout > config.timeout_seconds:
        return (
            f"Requested timeout ({requested_timeout}s) exceeds limit "
            f"({config.timeout_seconds}s) for scan type '{scan_type}'."
        )
    return None


def validate_concurrency(scan_type: str, requested_concurrency: int) -> Optional[str]:
    """Return error message if requested concurrency exceeds scan type limit."""
    config = SCAN_TYPES.get(scan_type)
    if config is None:
        return f"Unknown scan type '{scan_type}'."
    if not isinstance(requested_concurrency, int) or requested_concurrency < 1:
        return "max_concurrency must be a positive integer."
    if requested_concurrency > config.max_concurrency:
        return (
            f"Requested concurrency ({requested_concurrency}) exceeds limit "
            f"({config.max_concurrency}) for scan type '{scan_type}'."
        )
    return None


def validate_manual_audit_guard(
    scan_type: str,
    *,
    manual_review_flag: bool = False,
    authorization_placeholder: bool = False,
) -> Optional[str]:
    """Return error message if manual_audit_assisted is requested without proper authorization."""
    if scan_type != ScanType.MANUAL_AUDIT_ASSISTED:
        return None
    if not manual_review_flag and not authorization_placeholder:
        return (
            "Scan type 'manual_audit_assisted' requires the manual_review flag "
            "or explicit authorization. This scan type is not available for public self-serve."
        )
    return None


def validate_retest_categories(
    scan_type: str,
    requested_categories: List[str],
) -> Optional[str]:
    """Return error message if retest_scan requests overly broad categories."""
    if scan_type != ScanType.RETEST_SCAN:
        return None
    if not requested_categories:
        return "Scan type 'retest_scan' requires at least one targeted category."
    if len(requested_categories) > 3:
        return (
            f"Scan type 'retest_scan' allows at most 3 targeted categories, "
            f"but {len(requested_categories)} were requested. "
            "Use a standard or deep scan for broader coverage."
        )
    return None


def validate_payload_no_secrets(payload: Dict[str, Any]) -> Optional[str]:
    """Return error message if payload contains secret-looking fields."""
    flagged = contains_secret_looking_fields(payload)
    if flagged:
        return f"Payload contains secret-looking fields: {', '.join(flagged)}. Remove secrets from scan requests."
    return None


# ---------------------------------------------------------------------------
# Composite validator
# ---------------------------------------------------------------------------

def validate_scan_request(
    scan_type: str,
    *,
    verification_status: str = "unverified",
    requested_categories: Optional[List[str]] = None,
    requested_max_tests: Optional[int] = None,
    requested_timeout: Optional[int] = None,
    requested_concurrency: Optional[int] = None,
    manual_review_flag: bool = False,
    manual_authorization_override: bool = False,
    payload: Optional[Dict[str, Any]] = None,
) -> ScanLimitValidationResult:
    """Run all scan limit validations and return an aggregated result."""
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Scan type exists
    err = validate_scan_type_exists(scan_type)
    if err:
        return ScanLimitValidationResult(valid=False, errors=[err])

    config = get_scan_type(scan_type)
    assert config is not None  # guaranteed by check above

    # 2. Scan type enabled
    err = validate_scan_type_enabled(scan_type)
    if err:
        errors.append(err)

    # 3. Target verified
    err = validate_target_verified(
        scan_type,
        verification_status,
        manual_authorization_override=manual_authorization_override,
    )
    if err:
        errors.append(err)

    # 4. Categories allowed
    if requested_categories is not None:
        err = validate_categories_allowed(scan_type, requested_categories)
        if err:
            errors.append(err)

    # 5. Max tests
    if requested_max_tests is not None:
        err = validate_max_tests(scan_type, requested_max_tests)
        if err:
            errors.append(err)

    # 6. Timeout
    if requested_timeout is not None:
        err = validate_timeout(scan_type, requested_timeout)
        if err:
            errors.append(err)

    # 7. Concurrency
    if requested_concurrency is not None:
        err = validate_concurrency(scan_type, requested_concurrency)
        if err:
            errors.append(err)

    # 8. Manual audit guard
    err = validate_manual_audit_guard(
        scan_type,
        manual_review_flag=manual_review_flag,
        authorization_placeholder=manual_authorization_override,
    )
    if err:
        errors.append(err)

    # 9. Retest category restrictions
    if requested_categories is not None:
        err = validate_retest_categories(scan_type, requested_categories)
        if err:
            errors.append(err)

    # 10. Payload secret rejection
    if payload is not None:
        err = validate_payload_no_secrets(payload)
        if err:
            errors.append(err)

    return ScanLimitValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        resolved_scan_type=scan_type,
        resolved_config=config,
    )
