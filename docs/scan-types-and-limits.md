# Scan Types and Limits — Phase 16

## Overview

Phase 16 establishes the **scan type and limit system foundation** for PowerDetect Sherlock. It defines safe scan modes, plan-aware limits, category inclusion rules, worker job constraints, and validation helpers so future scan execution cannot become unlimited, expensive, abusive, or unsafe.

This phase is **limits and scan-mode foundation only**. It does not implement public scan execution, billing, Stripe, PDF/report generation, admin panels, production queue deployment, or real network scanning.

---

## Scan Types

### Quick Scan

- **Purpose**: Very small preflight check. Low cost, fast turnaround. Useful for early demo/free tier.
- **Max Tests**: 10
- **Timeout**: 120 seconds
- **Max Concurrency**: 1
- **Response Limit**: 4,000 chars/test
- **Categories**: Prompt Injection, System Prompt Leakage, Unsafe Output Handling
- **Verified Target**: Required
- **Report Level**: Summary
- **Status**: Enabled

### Standard Scan

- **Purpose**: Balanced launch-readiness scan covering core categories.
- **Max Tests**: 50
- **Timeout**: 600 seconds
- **Max Concurrency**: 2
- **Response Limit**: 8,000 chars/test
- **Categories**: Prompt Injection, System Prompt Leakage, Sensitive Data Leakage, RAG Data Leakage, Unsafe Output Handling, Cost Abuse
- **Verified Target**: Required
- **Report Level**: Standard
- **Status**: Enabled

### Deep Scan

- **Purpose**: Thorough review for serious AI applications. Broader coverage.
- **Max Tests**: 150
- **Timeout**: 1800 seconds
- **Max Concurrency**: 3
- **Response Limit**: 12,000 chars/test
- **Categories**: All 8 categories
- **Verified Target**: Required
- **Report Level**: Detailed
- **Status**: Disabled (requires future paid plan gate)

### Manual Audit Assisted

- **Purpose**: Semi-automated support for Phase 8 manual audit workflow.
- **Max Tests**: 250
- **Timeout**: 3600 seconds
- **Max Concurrency**: 2
- **Categories**: All 8 categories
- **Verified Target**: Required (or manual authorization override)
- **Manual Review**: Required
- **Report Level**: Manual Review
- **Status**: Disabled (not self-serve)

### Retest Scan

- **Purpose**: Focused retest for specific findings/categories after fixes.
- **Max Tests**: 20
- **Timeout**: 300 seconds
- **Max Concurrency**: 1
- **Response Limit**: 4,000 chars/test
- **Categories**: Targeted only (max 3 categories per retest)
- **Verified Target**: Required
- **Report Level**: Retest
- **Status**: Enabled

---

## Category Matrix

| Category | Quick | Standard | Deep | Manual Audit | Retest |
|---|---|---|---|---|---|
| Prompt Injection | ✓ | ✓ | ✓ | ✓ | Targeted |
| System Prompt Leakage | ✓ | ✓ | ✓ | ✓ | Targeted |
| Sensitive Data Leakage | — | ✓ | ✓ | ✓ | Targeted |
| RAG Data Leakage | — | ✓ | ✓ | ✓ | Targeted |
| Indirect Prompt Injection | — | — | ✓ | ✓ | Targeted |
| Tool / Function Abuse | — | — | ✓ | ✓ | Targeted |
| Unsafe Output Handling | ✓ | ✓ | ✓ | ✓ | Targeted |
| Cost Abuse | — | ✓ | ✓ | ✓ | Targeted |

Categories map to the Phase 6 prompt library manifest in `packages/prompt_library/manifest.json`.

---

## Plan/Tier Placeholders

Plan tiers are **placeholders only**. Billing, Stripe, and real plan enforcement are NOT implemented. No paid plans are live.

| Tier | Scan Types | Monthly Scans | Max Projects | Retests | Web Report | PDF Export |
|---|---|---|---|---|---|---|
| Free | Quick | 3 | 1 | 0 | — | — |
| Launch Scan | Quick, Standard, Retest | 5 | 2 | 2 | ✓ | — |
| Builder | Quick, Standard, Deep, Retest | 20 | 5 | 10 | ✓ | ✓ |
| Startup | Quick, Standard, Deep, Retest | 50 | 15 | 25 | ✓ | ✓ |
| Manual Audit | All (including Manual Audit Assisted) | 100 | 25 | 50 | ✓ | ✓ |

---

## Limit Rationale

- **Every scan must be bounded.** No unbounded prompt execution, tool calls, or retries.
- **Every scan requires a verified target** unless manually authorized by an auditor.
- **Default free/demo scans must be small** — quick scan with 10 tests max.
- **Deep scans are gated** by plan/manual review to prevent cost abuse.
- **Job payloads must not contain secrets** — API keys, tokens, passwords are rejected.
- **Scanner must not run against unverified targets.**
- **External network scanning still requires SSRF protection and rate limits.**
- **Users must not control raw max_tests, timeout, or concurrency beyond server limits.**

---

## Validation Helpers

The `packages/scan_limits/validators.py` module provides composable validators:

- `validate_scan_type_exists` — scan type is recognized
- `validate_scan_type_enabled` — scan type is currently active
- `validate_target_verified` — target has passed ownership verification
- `validate_categories_allowed` — requested categories match scan type rules
- `validate_max_tests` — test count is within scan type limit
- `validate_timeout` — timeout is within scan type limit
- `validate_concurrency` — concurrency is within scan type limit
- `validate_manual_audit_guard` — manual audit requires authorization
- `validate_retest_categories` — retest cannot request overly broad categories
- `validate_payload_no_secrets` — payload does not contain secret-looking fields
- `validate_scan_request` — composite validator running all checks

---

## Worker Integration

Phase 16 adds a `scan_type_limits` safety gate to the Phase 15 worker pipeline. This gate:

- Validates job payloads against scan type limit definitions
- Is backward-compatible with `safe_smoke` mock scans from Phase 15
- Runs after existing Phase 15 gates (queue_enabled, target_verified, etc.)
- Does not create real scan jobs or trigger production workers

Integration module: `packages/scan_limits/worker_integration.py`

---

## API Endpoints

Phase 16 adds two safe, static GET endpoints:

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v0/scans/types` | List available scan types and their limits |
| GET | `/api/v0/scans/limits` | Get scan limits, plan tier info, and category matrix |

Both endpoints return static Phase 16 metadata. They do not create scan jobs, trigger workers, or require authentication.

---

## Environment Configuration

| Variable | Default | Purpose |
|---|---|---|
| `SCAN_LIMITS_ENABLED` | `true` | Enable scan limit validation |
| `DEFAULT_SCAN_TYPE` | `quick_scan` | Default scan type for new scans |
| `MAX_SCAN_TESTS_PER_JOB` | `50` | Server-wide maximum tests per scan job |
| `MAX_SCAN_TIMEOUT_SECONDS` | `600` | Server-wide maximum timeout |
| `MAX_SCAN_CONCURRENCY` | `2` | Server-wide maximum concurrency |
| `FREE_TIER_MONTHLY_SCANS` | `3` | Monthly scan limit for free tier placeholder |
| `DEEP_SCAN_ENABLED` | `false` | Whether deep scan is enabled |

---

## Files

### Created
- `packages/scan_limits/__init__.py` — package exports
- `packages/scan_limits/scan_types.py` — scan type definitions and limits
- `packages/scan_limits/categories.py` — category registry and scan-type mapping
- `packages/scan_limits/plans.py` — plan/tier placeholder definitions
- `packages/scan_limits/validators.py` — scan limit validation helpers
- `packages/scan_limits/worker_integration.py` — worker system safety gate integration
- `packages/scan_limits/tests/__init__.py` — test package init
- `packages/scan_limits/tests/test_scan_limits.py` — 82 unit tests
- `apps/web/dashboard/scan-setup.html` — scan type selection and limits UI shell
- `docs/scan-types-and-limits.md` — this document

### Modified
- `packages/worker_system/safety.py` — added scan_type_limits gate
- `apps/api/app/schemas/scans.py` — added ScanTypeEntry, PlanTierEntry schemas
- `apps/api/app/routes/scans.py` — added GET /scans/types and GET /scans/limits
- `apps/api/app/routes/version.py` — updated scans module status
- `apps/api/app/config.py` — added scan_limits_enabled, default_scan_type, deep_scan_enabled
- `apps/api/app/main.py` — updated description
- `apps/web/dashboard/scans.html` — Phase 16 banner and scan setup link
- `apps/web/dashboard/index.html` — Phase 16 banner and activity timeline
- `.env.example` — Phase 16 scan limit placeholders
- `config/product.json` — updated phase
- `docs/roadmap.md` — Phase 16 entry
- `docs/architecture.md` — Phase 16 scan limits section
- `docs/security.md` — Phase 16 scan limit security notes
- `docs/workers.md` — Phase 16 integration notes
- `apps/api/README.md` — Phase 16 notes
- `apps/web/README.md` — scan setup page reference
- `README.md` — Phase 16 status

---

## What Is Intentionally Not Live Yet

- Public scan execution
- Real external target scanning
- Production billing / Stripe
- Paid plan enforcement
- PDF/report generation
- Admin panel
- Findings persistence or web reports
- Production queue deployment
- Scanner execution from public API
- Service-role usage in frontend
- Real secret storage
- SSRF-hardened target fetching
- Automatic paid plan enforcement

---

## Future Integration

- **Phase 17 (Findings)**: Completed foundation. Findings can retain source scan/test IDs and future scan type metadata while staying separate from active scan execution.
- **Phase 18 (Web Report)**: Completed foundation. Report level from scan type config can inform future report detail level, but Phase 18 does not run scans or persist reports.
- **Phase 21 (Billing)**: Plan tier enforcement connected to Stripe.
- **Phase 22 (Hardening)**: SSRF protection, rate limits, spend controls, audit logging.
- **Future**: Dynamic limit overrides from database or admin configuration.
