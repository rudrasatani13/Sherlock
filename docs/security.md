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
- The Phase 9 backend API includes placeholder target and verification route groups only. It does not implement production target verification or unlock public scanning.
- Phase 13 target setup UI captures metadata and acknowledgement placeholders only. It does not verify ownership, prove authorization, unlock scans, or test targets.
- Phase 14 defines verification method contracts (DNS TXT, HTML meta tag, well-known file, manual authorization, chatbot/API challenge), challenge token design, and safe validation helpers. It does not perform production DNS/HTTP/chatbot verification checks, persist verification records, or unlock scanning.
- Phase 14 adds target ownership verification foundation (method definitions, validation helpers, challenge tokens, API contract, UI). No real verification checks are performed — production DNS, HTTP, and chatbot verification require future SSRF-safe network utilities.
- Phase 15 adds queue/worker safety gates:
  - target must be verified before scan jobs execute
  - private/internal/localhost/metadata URLs are blocked
  - secret-looking fields (API keys, tokens, passwords) rejected from payloads
  - configurable max_tests and timeout_seconds limits
  - WORKER_ENABLED must be true for production job dispatch
  - full SSRF hardening (DNS rebinding, redirect following) deferred to Phase 22
- Challenge tokens use the format `sherlock_<random_urlsafe_token>` and are proof-of-control values, not secrets. Tokens should expire, be stored hashed if persisted, be scoped to target and method, and not grant access by themselves.
- Verification attempts should be rate-limited in future phases to prevent abuse.
- Verification logs may contain sensitive target metadata and should be protected.
- Manual review is required for ambiguous targets.

## Network Safety

- Prevent SSRF before adding URL or API scanning.
- Block private, internal, link-local, loopback, and metadata service IP ranges before allowing scan requests.
- Resolve and validate redirects, DNS rebinding behavior, and user-supplied hostnames.
- Add explicit timeouts, body limits, retry limits, and concurrency limits.
- Do not expose scanner execution through API routes until ownership verification, SSRF protection, rate limits, spend controls, authorization, and production queue workers exist. Phase 15 provides a local queue/worker foundation with safety gates but does not unlock public scan execution.

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
- Phase 12 auth UI pages are static shells only. They must not store passwords, tokens, real Supabase keys, service-role keys, or fake user IDs in browser code.
- Phase 13 project/target setup pages are static shells only. They must not store real API keys, bearer tokens, cookies, passwords, private keys, raw headers, target credentials, or production secrets in frontend code or committed files.
- Phase 14 verification UI is a static shell only. It must not issue real challenges, perform real DNS/HTTP/chatbot checks, store verification records, or persist challenge tokens in frontend code or committed files.
- Phase 17 findings objects must store only redacted, report-safe evidence summaries by default. Do not store raw headers, cookies, API keys, bearer tokens, private keys, private documents, large transcripts, generated reports, scan outputs, evaluator outputs, or real customer evidence in Git.

## Authentication and Accounts

- Phase 11 selects Supabase Auth as the intended auth provider and adds a backend auth foundation only.
- Supabase Auth stores identity users in the Supabase-managed `auth` schema.
- Sherlock app-level user metadata belongs in `public.user_profiles` and tenant access belongs in `public.organization_members`.
- `GET /api/v0/auth/status` is public and returns configuration state only.
- `GET /api/v0/me` is a protected route foundation and must not return fake users when auth is disabled or incomplete.
- Backend routes must validate Supabase-issued JWTs before trusting user identity in future production phases.
- Never trust user IDs supplied in request bodies for authentication or tenant authorization.
- Phase 12 adds login, signup, forgot-password, and dashboard UI shells only; it does not add production auth/session flow.
- Phase 13 adds project and target setup UI only; it does not add production auth/session flow or authenticated project persistence.
- Phase 14 adds verification contracts and UI only; it does not add production verification checks, verification persistence, or authenticated verification flows.
- Do not add production OAuth provider setup, sessions, browser token handling, or broad RLS policies until a reviewed future phase.

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
- Phase 17 enforces critical/high evidence and fix-guidance requirements in the internal findings model. Critical severity requires a strong evidence marker or manual review flag.
- Low-confidence observations should be marked for manual review or treated as inconclusive unless impact is independently confirmed.
- System prompt leakage is not automatically critical. Severity depends on what leaked and what impact the leakage enables.

## Cost and Abuse Controls

- Add spend limits before automated scanner execution.
- Add rate limits before public scan creation.
- Add cancellation and timeout support before long-running scans.
- Do not allow unbounded prompt loops, tool calls, or retries.
- Keep Phase 9 scan routes as `501 not_implemented` placeholders until abuse controls and worker isolation are added.
- Phase 16 adds scan type limit definitions, category inclusion rules, plan tier placeholders, and validation helpers under `packages/scan_limits`:
  - every scan type has bounded max_tests, timeout_seconds, max_concurrency, and response char limits
  - every scan type requires a verified target (manual_audit_assisted allows auditor authorization override)
  - quick scans are limited to 10 tests and 120 seconds
  - deep scans are disabled until paid plan gates exist
  - manual_audit_assisted is not self-serve and requires manual review flag or authorization
  - retest scans require targeted categories (max 3) and cannot request broad coverage
  - job payloads are validated against scan type limits before worker execution
  - plan tiers are placeholders — billing and Stripe are not implemented
  - users cannot set raw max_tests, timeout, or concurrency beyond server-defined limits

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
- Phase 10 adds a database schema and migration foundation under `db/`, Phase 11 adds Supabase Auth-compatible backend placeholders under `apps/api`, Phase 12 adds a static dashboard/auth UI shell under `apps/web`, Phase 13 adds static project/target setup pages plus placeholder API contract metadata, Phase 14 adds verification contracts, safe validation helpers, and verification UI, Phase 16 adds scan type definitions, limit validation helpers, plan tier placeholders, GET /scans/types and GET /scans/limits endpoints, and a scan_type_limits worker safety gate, and Phase 17 adds static findings schema metadata plus an internal findings package. The API still does not implement active database persistence, active findings persistence, real production project persistence, production JWT verification, production DNS/HTTP/chatbot verification checks, verification record persistence, billing, public scan execution, scanner execution, real report generation, PDF export, admin panels, or real customer evidence storage.
- Future scanner integration must run outside public request handlers and only after production auth, authorization, ownership verification, SSRF protection, rate limits, spend controls, audit logging, and worker queues are in place.
