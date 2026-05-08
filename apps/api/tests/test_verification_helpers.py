"""Phase 14 unit tests for safe verification helpers.

These tests verify challenge token generation, hashing, and format/method/status
validation without any network requests.
"""
from __future__ import annotations

import unittest

from app.verification import (
    ALLOWED_VERIFICATION_METHODS,
    ALLOWED_VERIFICATION_STATUSES,
    CHALLENGE_PREFIX,
    generate_challenge_token,
    hash_challenge_token,
    is_valid_challenge_format,
    is_valid_verification_method,
    is_valid_verification_status,
)


class VerificationHelperTests(unittest.TestCase):
    def test_generate_challenge_token_has_prefix(self) -> None:
        token = generate_challenge_token()
        self.assertTrue(token.startswith(CHALLENGE_PREFIX))

    def test_generate_challenge_token_is_unique(self) -> None:
        tokens = {generate_challenge_token() for _ in range(50)}
        self.assertEqual(len(tokens), 50)

    def test_generate_challenge_token_valid_format(self) -> None:
        for _ in range(20):
            self.assertTrue(is_valid_challenge_format(generate_challenge_token()))

    def test_hash_challenge_token_deterministic(self) -> None:
        token = generate_challenge_token()
        self.assertEqual(hash_challenge_token(token), hash_challenge_token(token))

    def test_hash_challenge_token_different_for_different_tokens(self) -> None:
        a = generate_challenge_token()
        b = generate_challenge_token()
        self.assertNotEqual(hash_challenge_token(a), hash_challenge_token(b))

    def test_hash_challenge_token_is_hex(self) -> None:
        h = hash_challenge_token("sherlock_test123")
        self.assertEqual(len(h), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in h))

    def test_is_valid_challenge_format_accepts_valid(self) -> None:
        self.assertTrue(is_valid_challenge_format("sherlock_aBcDeFgHiJkLmNoPqRsT"))
        self.assertTrue(is_valid_challenge_format("sherlock_abcdefgh12345678"))
        self.assertTrue(is_valid_challenge_format("sherlock_" + "a" * 32))

    def test_is_valid_challenge_format_rejects_invalid(self) -> None:
        self.assertFalse(is_valid_challenge_format(""))
        self.assertFalse(is_valid_challenge_format("sherlock_"))
        self.assertFalse(is_valid_challenge_format("badprefix_abc123def456ghij"))
        self.assertFalse(is_valid_challenge_format("sherlock_has spaces here"))
        self.assertFalse(is_valid_challenge_format("sherlock_tooshort"))

    def test_is_valid_verification_method(self) -> None:
        for m in ALLOWED_VERIFICATION_METHODS:
            self.assertTrue(is_valid_verification_method(m))
        self.assertFalse(is_valid_verification_method("invalid_method"))
        self.assertFalse(is_valid_verification_method(""))

    def test_is_valid_verification_status(self) -> None:
        for s in ALLOWED_VERIFICATION_STATUSES:
            self.assertTrue(is_valid_verification_status(s))
        self.assertFalse(is_valid_verification_status("approved"))
        self.assertFalse(is_valid_verification_status(""))

    def test_allowed_methods_complete(self) -> None:
        expected = {"dns_txt", "html_meta_tag", "well_known_file", "manual_authorization", "chatbot_api_challenge"}
        self.assertEqual(ALLOWED_VERIFICATION_METHODS, expected)

    def test_allowed_statuses_complete(self) -> None:
        expected = {"unverified", "pending", "verified", "failed", "expired", "manual_review_required"}
        self.assertEqual(ALLOWED_VERIFICATION_STATUSES, expected)


if __name__ == "__main__":
    unittest.main()
