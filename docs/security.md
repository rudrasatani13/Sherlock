# Security Notes

Sherlock will eventually test AI systems that may connect to customer data, tools, internal APIs, and sensitive workflows. Security controls must be designed before real scanning is exposed to customers.

## Secrets

- Do not store API keys, provider tokens, database credentials, webhook secrets, or private keys in plain text.
- Do not commit `.env.local`, `.env.production`, or any real environment file.
- Use `.env.example` for placeholder values only.
- Prefer managed secret storage in deployed environments.

## Target Authorization

- Require ownership verification before scanning any URL, API, chatbot, RAG app, agent, or customer system.
- Keep verification state auditable.
- Do not run external scans against unverified targets.
- The Phase 5 internal scanner must only be used against targets the operator owns or is explicitly authorized to test.
- Phase 8 manual audits require written authorization, approved scope, testing windows, rate limits, escalation contacts, and documented out-of-scope targets before testing.
- The Phase 9 backend API includes placeholder target and verification route groups only. It does not implement target verification or unlock public scanning.

## Network Safety

- Prevent SSRF before adding URL or API scanning.
- Block private, internal, link-local, loopback, and metadata service IP ranges before allowing scan requests.
- Resolve and validate redirects, DNS rebinding behavior, and user-supplied hostnames.
- Add explicit timeouts, body limits, retry limits, and concurrency limits.
- Do not expose scanner execution through API routes until ownership verification, SSRF protection, rate limits, spend controls, authorization, and queue workers exist.

## Data Handling

- Scan logs may contain sensitive data.
- Store only what is necessary for evidence and debugging.
- Redact sensitive evidence in reports.
- Avoid retaining raw prompts, responses, headers, tokens, cookies, and uploaded files unless there is a clear reason and customer consent.
- Generated scan outputs and reports should not be committed.
- Phase 5 local scan outputs may contain sensitive target responses and should stay in ignored, protected folders such as `scan-results/`.
- Phase 8 audit evidence, completed client templates, authorization notes, report drafts, screenshots, and retest records may contain sensitive data and should stay outside Git.
- Phase 9 API responses are static foundation responses and placeholders. They should not include customer data, target secrets, raw scan evidence, generated reports, or evaluator output.
- Phase 10 database migrations and seeds must not contain real secrets, real target credentials, real customer data, raw evidence, scan outputs, evaluator outputs, or report drafts.
- Phase 11 auth placeholders must not contain real Supabase keys. Keep real auth values only in ignored local or managed deployment environments.
- The Supabase service-role key is server-only and must never be exposed to browser/frontend code.

## Authentication and Accounts

- Phase 11 selects Supabase Auth as the intended auth provider and adds a backend auth foundation only.
- Supabase Auth stores identity users in the Supabase-managed `auth` schema.
- Sherlock app-level user metadata belongs in `public.user_profiles` and tenant access belongs in `public.organization_members`.
- `GET /api/v0/auth/status` is public and returns configuration state only.
- `GET /api/v0/me` is a protected route foundation and must not return fake users when auth is disabled or incomplete.
- Backend routes must validate Supabase-issued JWTs before trusting user identity in future production phases.
- Never trust user IDs supplied in request bodies for authentication or tenant authorization.
- Do not add production OAuth provider setup, login/signup UI, sessions, or broad RLS policies until a reviewed future phase.

## Database Security

- Phase 10 adds PostgreSQL/Supabase-compatible schema and migration files only.
- Do not store target API keys, bearer tokens, cookies, passwords, private keys, raw headers, or session material in plain text.
- Future target credentials must use managed secret storage or encrypted storage.
- RLS is enabled in the initial migration, but production user policies are not implemented yet.
- Phase 11 keeps RLS deny-by-default and documents future policies based on `auth.uid()` and organization membership.
- Do not expose the database publicly without authentication, authorization, tenant-scoped RLS, and server-side access checks.
- Raw scan evidence should not be stored by default because prompts, responses, retrieval traces, tool traces, and screenshots may contain sensitive data.
- Store only report-safe redacted evidence summaries unless a future phase explicitly designs protected raw-evidence storage with retention and deletion controls.
- Data retention and deletion workflows remain future work.

## Reporting Language

- Reports must not claim "your AI app is secure."
- Passing a scan does not guarantee complete security.
- Findings should describe observed behavior, evidence, impact, limitations, and recommended remediation.
- Reports should use plain English, include tested scope, and avoid fearmongering or overclaiming.
- Reports should not claim "100% protected", "certified safe", "all vulnerabilities found", or "no risk exists."

## Severity and Confidence

- Use the severity and confidence systems in `docs/methodology.md`.
- Do not mark a finding Critical unless there is strong evidence of serious impact such as customer data exposure, unauthorized action, credential leakage, or major business risk.
- Low-confidence observations should be marked for manual review or treated as inconclusive unless impact is independently confirmed.
- System prompt leakage is not automatically critical. Severity depends on what leaked and what impact the leakage enables.

## Cost and Abuse Controls

- Add spend limits before automated scanner execution.
- Add rate limits before public scan creation.
- Add cancellation and timeout support before long-running scans.
- Do not allow unbounded prompt loops, tool calls, or retries.
- Keep Phase 9 scan routes as `501 not_implemented` placeholders until abuse controls and worker isolation are added.

## Tool and Function Abuse

Future tool-using-agent tests must avoid invoking destructive or high-risk actions unless the test target is isolated and explicitly authorized. Scanner design should make side effects visible and controllable.

## Manual Audit Workflow

- Use `docs/audits/README.md` as the Phase 8 manual audit workflow reference.
- Do not begin manual or semi-automated testing until intake, authorization, scope, data handling, and pause conditions are documented.
- Use safe defensive playbooks only.
- Do not test unauthorized third-party systems.
- Do not commit raw evidence, generated scan outputs, evaluator outputs, completed client templates, authorization records, or report drafts containing client data.

## Backend API Boundary

- Phase 9 adds a FastAPI foundation under `apps/api` with health, version/status, config, logging, CORS placeholder, structured errors, response schemas, and placeholder route groups.
- Phase 10 adds a database schema and migration foundation under `db/`, and Phase 11 adds Supabase Auth-compatible backend placeholders under `apps/api`, but the API still does not implement active database persistence, production JWT verification, dashboard integration, billing, queue workers, target verification, public scan execution, scanner execution, real report generation, PDF export, or admin panels.
- Future scanner integration must run outside public request handlers and only after production auth, authorization, ownership verification, SSRF protection, rate limits, spend controls, audit logging, and worker queues are in place.
