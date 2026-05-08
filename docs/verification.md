# Target Ownership Verification — Phase 14

## Overview

Phase 14 establishes the **target ownership verification** foundation for PowerDetect Sherlock. Verification proves that a user controls or is authorized to test a target before any scan can run.

This phase delivers:

- Verification method definitions (DNS TXT, HTML meta tag, well-known file, manual authorization, chatbot/API challenge)
- Verification status lifecycle (unverified → pending → verified / failed / expired / manual_review_required)
- Challenge token format and security design
- API contract placeholders (request/response schemas)
- Safe validation helpers (token generation, hashing, format checks — no network requests)
- Static dashboard UI for method selection, instructions, and status display
- Unit tests for non-network verification helpers

This phase does **not** deliver production DNS/HTTP/chatbot verification checks, active API persistence, scan unlocking, or SSRF-safe network requests.

---

## Verification Methods

| Method | Key | Network Check | Implemented |
|---|---|---|---|
| DNS TXT Record | `dns_txt` | Yes (future) | No |
| HTML Meta Tag | `html_meta_tag` | Yes (future) | No |
| Well-Known File | `well_known_file` | Yes (future) | No |
| Manual Authorization Review | `manual_authorization` | No | No |
| Chatbot/API Challenge | `chatbot_api_challenge` | Yes (future) | No |

### DNS TXT Record

- User adds a TXT record to the target domain: `sherlock-verification=<challenge>`.
- DNS propagation may take minutes to hours.
- Future backend will check DNS safely after SSRF protections exist.

### HTML Meta Tag

- User adds `<meta name="sherlock-verification" content="<challenge>">` inside `<head>` on the target homepage.
- Future backend will fetch and verify only after SSRF protections exist.

### Well-Known File

- User creates `/.well-known/sherlock-verification.txt` with content `sherlock-verification=<challenge>`.
- Future backend will verify only after SSRF protections exist.

### Manual Authorization Review

- User provides authorization documents, legal/scope confirmation, contact person, allowed targets, testing window, and forbidden actions.
- An operator reviews manually.
- File upload and admin review are not implemented in this phase.

### Chatbot/API Challenge

- Sherlock sends a safe challenge message: `Return verification code exactly: <challenge>`.
- Target must respond with the exact challenge string.
- Real challenge execution must wait for network safety controls.

---

## Verification Status Lifecycle

| Status | Description |
|---|---|
| `unverified` | No verification attempt has been made. |
| `pending` | A verification challenge has been created and is awaiting proof. |
| `verified` | Ownership proof was accepted. Scanning may be unlocked in a future phase. |
| `failed` | The verification check did not succeed. |
| `expired` | The challenge or verification has expired and must be retried. |
| `manual_review_required` | Manual authorization review is needed. |

---

## Challenge Token Design

- **Format:** `sherlock_<random_urlsafe_base64_token>` (24 bytes of randomness)
- **Example:** `sherlock_aBcDeFgHiJkLmNoPqRsT`
- Tokens are **proof-of-control** values, not secrets.
- Tokens should **expire** after a configured TTL.
- Tokens should be **stored hashed** (SHA-256) if persisted to the database.
- Tokens are **scoped** to a specific target and verification method.
- Tokens **do not grant access** by themselves.

---

## API Contract Placeholders

The `GET /api/v0/verification` endpoint returns a `501 not_implemented` response with the full verification contract as structured details, including:

- `VerificationMethodRegistry` — supported methods
- `VerificationStatusRegistry` — status definitions
- `ChallengeTokenDesign` — token format and security notes
- `CreateVerificationChallengeRequest` — future request contract
- `VerificationChallengeResponse` — future response contract
- `VerificationStatusResponse` — future status response contract

No route creates, persists, or checks verification records in this phase.

---

## Database Foundation

Phase 10 already defines the `target_verifications` table with:

- `id` (UUID)
- `target_id` (FK to `targets`)
- `verification_type` (text)
- `status` (enum: pending, verified, failed, expired)
- `challenge_hash` (text)
- `challenge_reference` (text)
- `verified_at` (timestamptz)
- `expires_at` (timestamptz)
- `created_at` (timestamptz)

Phase 14 does not modify the database schema. The existing enum does not include `unverified` or `manual_review_required` — these are tracked at the application/contract level. A future migration may extend the enum if needed.

---

## Safe Validation Helpers

`apps/api/app/verification.py` provides:

- `generate_challenge_token()` — random URL-safe token with `sherlock_` prefix
- `hash_challenge_token(token)` — SHA-256 hex digest for safe storage
- `is_valid_challenge_format(token)` — regex format check
- `is_valid_verification_method(method)` — allowed method check
- `is_valid_verification_status(status)` — allowed status check

These helpers perform **no network requests** and are safe to use in any context.

---

## Security Boundaries

- **No scan without verified target.** Scanning is blocked until the target passes ownership verification.
- **No third-party target testing.** Users can only verify and scan targets they own or are authorized to test.
- **No automatic crawling without SSRF controls.** No HTTP fetch, DNS lookup, or API probing occurs until SSRF-safe controls are implemented.
- **No fetching private/internal IPs.** Localhost, internal metadata endpoints, and private networks are blocked.
- **No destructive actions during verification.**
- **No secrets in challenge values.** Challenge tokens are proof-of-control, not secrets.
- **Challenges should be random, short-lived, and non-sensitive.**
- **Verification attempts should be rate-limited** in future phases to prevent abuse.
- **Verification logs may contain sensitive target metadata** and should be protected.
- **Manual review needed for ambiguous targets.**

---

## UI Wording Guidelines

**Avoid:**
- "Verified secure"
- "Safe to scan"
- "Fully authorized"
- "Guaranteed owner"

**Use:**
- "Verification proves control of this target method."
- "Scanning remains disabled until verification is complete and future scan controls are implemented."
- "Passing verification does not mean the app is secure."

---

## Dashboard Pages

| Page | Phase 14 Changes |
|---|---|
| `target-verification.html` | **New.** Verification method selector, instructions per method, challenge token info, verification status card, history placeholder, security boundaries. |
| `target-detail.html` | Updated verification status, link to verification page, progress step. |
| `target-setup.html` | Updated to link to verification as next step. |
| `project-detail.html` | Updated verification status and target table actions. |
| `projects.html` | Updated verification pills and progress step. |
| `index.html` | Updated banner and activity list for Phase 14. |

---

## What Remains for Future Phases

- **Phase 15:** Scan execution (requires verified targets, queue workers, SSRF protections, rate limits, spend controls)
- **Future:** Production DNS/HTTP/chatbot verification backend checks
- **Future:** Active API persistence of verification records
- **Future:** SSRF-safe network request utilities
- **Future:** Rate-limited verification attempts
- **Future:** Challenge token TTL enforcement
- **Future:** Manual authorization file upload and admin review
- **Future:** Verification audit logging

---

## Files

### Created
- `docs/verification.md` — this document
- `apps/web/dashboard/target-verification.html` — verification page
- `apps/api/app/verification.py` — safe validation helpers
- `apps/api/tests/test_verification_helpers.py` — helper unit tests

### Modified
- `apps/api/app/schemas/verification.py` — full contract schemas
- `apps/api/app/routes/verification.py` — updated route with contract details
- `apps/api/app/routes/version.py` — updated verification module status
- `apps/api/tests/test_api_foundation.py` — added verification contract test
- `apps/web/dashboard/target-detail.html` — Phase 14 verification links
- `apps/web/dashboard/target-setup.html` — Phase 14 verification links
- `apps/web/dashboard/project-detail.html` — Phase 14 verification links
- `apps/web/dashboard/projects.html` — Phase 14 verification status
- `apps/web/dashboard/index.html` — Phase 14 activity update
