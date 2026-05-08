# Sherlock Backend API

Status: Phase 14 Target Ownership Verification completed; API remains a placeholder backend foundation

This app is the minimal backend API foundation for Sherlock, the AI Launch Security Audit + Scanner product under the PowerDetect brand.

It introduces a small FastAPI application that future phases can extend for projects, targets, scans, findings, reports, verification, billing callbacks, and worker integration. Phase 10 adds a database schema foundation under `../../db`. Phase 11 adds Supabase Auth-compatible auth placeholders and current-user route foundations. Phase 12 adds a static dashboard/auth UI shell under `../web`, which may safely display `GET /api/v0/auth/status` when the local API is running. Phase 13 refines project and target placeholder route details with setup-contract metadata. The API still does not implement the full platform or active persistence.

## Scope

Phase 9 through Phase 14 include:

- FastAPI app skeleton under `apps/api`
- health and version/status endpoints
- public auth configuration status endpoint
- protected current-user route foundation
- placeholder route modules for future product areas
- shared response envelope with `success`, `data`, `error`, and `metadata`
- basic config loading from safe environment variables, including database and Supabase Auth placeholders
- structured error handling for validation, not found, not implemented, and internal errors
- basic logging setup
- local-only CORS placeholder configuration
- lightweight unittest coverage for config, health, version, auth helpers, and placeholder behavior
- Phase 10 database schema and migration documentation under `../../db`
- Phase 11 auth architecture documentation under `../../docs/auth.md`
- Phase 13 project/target setup contract metadata on placeholder responses
- Phase 14 verification method registry, status definitions, challenge token design, and request/response contract schemas
- Phase 14 safe verification helpers (token generation, hashing, format checks — no network requests)
- Phase 14 verification helper unit tests

Phase 14 adds verification contracts and safe helpers to placeholder responses. The API still does not include:

- active API database persistence
- real production project persistence
- target persistence from the UI
- production login/signup endpoints
- production JWT verification
- sessions
- project/report authorization enforcement
- billing or Stripe callbacks
- authenticated dashboard API integration
- queue workers or background jobs
- public scan execution
- production DNS/HTTP/chatbot verification checks
- verification record persistence
- SSRF protection implementation
- secret storage
- real report generation
- PDF export
- admin panel
- scanner execution through HTTP routes

## Structure

```text
apps/api/
|-- README.md
|-- requirements.txt
|-- app/
|   |-- __init__.py
|   |-- auth.py
|   |-- config.py
|   |-- errors.py
|   |-- logging.py
|   |-- main.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- auth.py
|   |   |-- findings.py
|   |   |-- health.py
|   |   |-- projects.py
|   |   |-- reports.py
|   |   |-- scans.py
|   |   |-- targets.py
|   |   |-- verification.py
|   |   `-- version.py
|   |-- verification.py        # Phase 14 safe validation helpers
|   `-- schemas/
|       |-- __init__.py
|       |-- auth.py
|       |-- common.py
|       |-- findings.py
|       |-- projects.py
|       |-- reports.py
|       |-- scans.py
|       |-- targets.py
|       `-- verification.py
`-- tests/
    |-- __init__.py
    |-- test_api_foundation.py
    `-- test_verification_helpers.py
```

## Local Setup

From the repository root, install the API dependencies into a local Python environment:

```bash
python3 -m pip install -r apps/api/requirements.txt
```

Run the API locally:

```bash
PYTHONPATH=apps/api python3 -m uvicorn app.main:app --reload --port 8000
```

Open the generated FastAPI docs locally:

```text
http://localhost:8000/docs
```

Apply the Phase 10 database migration locally only if you have a safe local PostgreSQL/Supabase-compatible database:

```bash
createdb sherlock_local
psql "postgresql://localhost/sherlock_local" -v ON_ERROR_STOP=1 -f db/migrations/20260507100000_phase_10_initial_database_foundation.sql
```

## Safe Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Confirms the API process is running and returns app name, status, version, and environment. |
| GET | `/version` | Returns current product phase, available modules, future placeholders, and disabled security-sensitive capabilities. |
| GET | `/api/v0/auth/status` | Returns Supabase Auth configuration state without requiring live credentials. |

## Protected Route Foundations

These routes are auth foundations only:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v0/me` | Future current-user response after Supabase JWT validation is implemented. |

With `AUTH_ENABLED=false` or missing Supabase/JWKS configuration, `/api/v0/me` returns `503 auth_unavailable`. It must not return fake users or trust arbitrary user IDs from request bodies.

## Placeholder Route Groups

These routes intentionally return `501 not_implemented` with a structured error response and capability details:

| Method | Path | Future purpose |
| --- | --- | --- |
| GET | `/api/v0/projects` | Future project/workspace records after database integration and auth exist. |
| GET | `/api/v0/targets` | Future target metadata and verified scope records. |
| GET | `/api/v0/scans` | Future scan job contracts and worker handoff after security controls exist. |
| GET | `/api/v0/findings` | Future reviewed findings system. |
| GET | `/api/v0/reports` | Future web report metadata and access contracts. |
| GET | `/api/v0/verification` | Phase 14 verification contract with method registry, status definitions, challenge token design, and request/response schemas. |

The project and target placeholder route details include Phase 13 setup-contract metadata. The verification placeholder route includes Phase 14 verification contracts with five supported methods (DNS TXT, HTML meta tag, well-known file, manual authorization, chatbot/API challenge), six statuses, challenge token design, and request/response schemas. No placeholder route persists data, triggers scanner execution, creates jobs, performs production verification checks, generates reports, stores secrets, or integrates with billing.

## Response Envelope

Responses use a shared shape for future consistency:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "metadata": {
    "api_version": "v0",
    "phase": "Phase 14 Target Ownership Verification completed",
    "environment": "local"
  }
}
```

Errors use the same envelope with `success: false` and an `error` object containing `code`, `message`, and optional `details`.

## Configuration

Safe environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SHERLOCK_APP_NAME` | `Sherlock` | Product/app name. |
| `SHERLOCK_BRAND` | `PowerDetect` | Brand/company identity. |
| `SHERLOCK_MARKETING_NAME` | `PowerDetect Sherlock` | Full marketing name. |
| `SHERLOCK_ENVIRONMENT` | `local` | Runtime environment label. |
| `SHERLOCK_API_VERSION` | `v0` | API route/version label. |
| `SHERLOCK_CURRENT_PHASE` | `Phase 14 Target Ownership Verification completed` | Product phase label. |
| `DATABASE_URL` | empty string | Local database URL placeholder for future persistence integration. Not used by routes in Phase 14. |
| `AUTH_ENABLED` | `false` | Enables future auth enforcement only after real Supabase/JWKS configuration exists. |
| `SUPABASE_URL` | empty string | Future Supabase project URL placeholder. |
| `SUPABASE_ANON_KEY` | empty string | Future browser-safe Supabase anon key placeholder. |
| `SUPABASE_SERVICE_ROLE_KEY` | empty string | Future server-only service-role key placeholder. Never expose to frontend code. |
| `SUPABASE_JWKS_URL` | empty string | Future JWKS URL for backend JWT verification. |
| `SHERLOCK_DEBUG` | `false` | Local debug flag. |
| `SHERLOCK_ALLOWED_ORIGINS` | `http://localhost:3000,http://localhost:4173` | Local CORS placeholder origins. |

No real secrets are required for Phase 14. Do not commit real database credentials, real Supabase keys, target credentials, API keys, bearer tokens, cookies, passwords, private keys, or raw auth headers.

## Auth Foundation

Supabase Auth is the intended provider.

Current behavior:

- `GET /api/v0/auth/status` reports configuration state and disabled capabilities.
- `GET /api/v0/me` is protected by `require_current_user`.
- `require_current_user` returns `auth_unavailable` while auth is disabled or JWT verification is not active.
- bearer-token parsing is strict and does not trust user IDs from request bodies.
- no service-role key is used in frontend/browser code.

Future production behavior should validate Supabase-issued JWTs against JWKS, load `public.user_profiles`, load `public.organization_members`, and enforce organization-scoped authorization before returning customer data.

## Tests

Run the API tests from the repository root:

```bash
PYTHONPATH=apps/api python3 -m unittest discover -s apps/api/tests
```

## Security Boundary

Scanner execution must not be exposed through this API until future phases add production authentication, authorization, target ownership verification, SSRF protection, rate limits, spend limits, audit logging, and queue workers.

The Phase 10 database migration enables RLS on application tables but does not add permissive user policies. Phase 11 keeps this deny-by-default posture. No route reads from or writes to the database yet.

The service-role key is backend-only and must never be exposed to browser/frontend code. Future RLS policies should use `auth.uid()` and organization membership to enforce tenant boundaries.

The Phase 12 static dashboard/auth UI, Phase 13 project/target setup UI, and Phase 14 verification UI must not use the service-role key, create fake sessions, trust browser-supplied user IDs, persist projects, persist targets, persist verification records, store secrets, perform production verification checks, or run scans. They may call only the public auth-status endpoint for configuration display.

The existing internal packages remain isolated:

- `packages/scanner_engine` may later be called by authenticated, authorized workers, not public request handlers.
- `packages/prompt_library` may later supply reviewed test cases after scope and target authorization exist.
- `packages/evaluator_system` may later process stored scanner observations and feed the findings system.

## Future Integration Notes

- Phase 10: database foundation and persistence contracts completed under `../../db`.
- Phase 11: authentication and user accounts foundation completed with Supabase Auth-compatible placeholders.
- Phase 12: static Dashboard V0 + Auth UI Shell completed under `../web`; production dashboard API consumption remains future work.
- Phase 13: static project/target setup UI and placeholder setup contracts completed. Active persistence and authenticated dashboard API consumption remain future work.
- Phase 14: verification contracts, safe validation helpers, verification UI, and documentation completed. Production DNS/HTTP/chatbot verification checks, verification persistence, and scan unlocking remain future work.
- Phase 15: add queue workers for scan execution outside request/response paths.
- Phase 17: add reviewed findings system using methodology, evaluator output, and manual review.
- Phase 18: add web report access after findings and access controls exist.
- Phase 21: add billing callbacks server-side after product flows are ready.
- Phase 22: add security hardening, abuse controls, audit logging, and production safeguards.
