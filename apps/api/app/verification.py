"""Phase 14 safe verification helpers.

This module provides challenge-token generation and format-validation utilities
that do NOT perform any network requests (DNS, HTTP, chatbot probing).

Real verification checks (DNS lookup, HTML fetch, API challenge) must wait until
SSRF-safe network utilities exist in a future phase.
"""
from __future__ import annotations

import hashlib
import re
import secrets


CHALLENGE_PREFIX = "sherlock_"
CHALLENGE_TOKEN_BYTES = 24
CHALLENGE_PATTERN = re.compile(r"^sherlock_[A-Za-z0-9_\-]{16,64}$")

ALLOWED_VERIFICATION_METHODS = frozenset({
    "dns_txt",
    "html_meta_tag",
    "well_known_file",
    "manual_authorization",
    "chatbot_api_challenge",
})

ALLOWED_VERIFICATION_STATUSES = frozenset({
    "unverified",
    "pending",
    "verified",
    "failed",
    "expired",
    "manual_review_required",
})


def generate_challenge_token() -> str:
    """Return a random URL-safe challenge token with the ``sherlock_`` prefix."""
    raw = secrets.token_urlsafe(CHALLENGE_TOKEN_BYTES)
    return f"{CHALLENGE_PREFIX}{raw}"


def hash_challenge_token(token: str) -> str:
    """Return a SHA-256 hex digest suitable for safe storage of a challenge token.

    Challenge tokens are proof-of-control values, not secrets, but hashing
    avoids storing raw tokens in the database if persistence is enabled later.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def is_valid_challenge_format(token: str) -> bool:
    """Check whether *token* matches the expected ``sherlock_<urlsafe>`` shape."""
    return bool(CHALLENGE_PATTERN.match(token))


def is_valid_verification_method(method: str) -> bool:
    """Return True if *method* is one of the Phase 14 supported methods."""
    return method in ALLOWED_VERIFICATION_METHODS


def is_valid_verification_status(status: str) -> bool:
    """Return True if *status* is one of the Phase 14 defined statuses."""
    return status in ALLOWED_VERIFICATION_STATUSES
