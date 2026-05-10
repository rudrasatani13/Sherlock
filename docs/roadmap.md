# Roadmap

This roadmap is directional. It should guide sequencing without forcing premature architecture decisions. `SHERLOCK_DEVELOPMENT_MASTER_PLAN.md` is the long-term product reference and phase source of truth. The current implementation represents **foundation versions** through Phase 19, not full production-complete versions of every expected output. See [Master Plan Alignment](master-plan-alignment.md) for details.

## Phase 1: Foundation

Status: completed

Goals:

- repository organization
- project overview
- architecture vision
- development setup notes
- security principles
- roadmap
- environment template
- ignore/config hygiene

Out of scope:

- scanner logic
- attack prompts
- evaluator logic
- API endpoints
- database migrations
- authentication
- dashboard UI
- billing
- queue workers
- reports
- PDF export
- target verification logic

## Phase 2: Landing/Public Website

Status: completed

Create the public-facing website for PowerDetect Sherlock with positioning, credibility, launch waitlist/contact path, and clear scope language.

Implemented as a static website under `apps/web`:

- homepage
- sample report page with demo-only content
- public methodology page
- security/trust page
- pricing and early-access page
- contact, beta, and audit request UI

Phase 2 did not implement scanner logic, attack prompts, evaluator logic, auth, dashboard, database, billing, queue workers, PDF generation, or real report generation.

## Phase 3: Methodology

Status: completed

Define the internal audit methodology, finding taxonomy, severity model, confidence model, evidence standards, remediation language, finding statuses, report language standards, and limitations beyond the public overview page.

Implemented as documentation only:

- detailed internal methodology in `docs/methodology.md`
- vulnerability category taxonomy
- evidence requirements
- severity, confidence, and status definitions
- report language standards
- future guidance for prompt library, evaluator, scanner engine, findings model, report generator, and manual audit workflow
- refreshed public methodology page language

Phase 3 did not implement scanner logic, attack prompts, evaluator logic, auth, dashboard, database, billing, queue workers, PDF generation, or real report generation.

## Phase 4: Sample Report

Status: completed

Create a more complete report structure and realistic static sample artifact that demonstrates expected output quality, evidence handling, redaction rules, disclaimer language, retest language, and future report expectations. The Phase 4 sample report remains demo-only and static.

Implemented as static content only:

- expanded public sample report page in `apps/web/sample-report.html`
- internal sample report reference in `docs/sample-report.md`
- fictional target app and demo findings
- sanitized evidence examples
- launch readiness verdict, score, severity breakdown, top fixes, findings table, detailed findings, retest status, tested scope, not-tested scope, limitations, and final recommendation

Phase 4 did not implement scanner logic, attack prompts, evaluator logic, auth, dashboard, database, billing, queue workers, PDF generation, backend report APIs, persistence, or real report generation.

## Phase 5: Internal Scanner

Status: completed

Built the first internal scanner foundation for controlled testing only. It includes scan configuration validation, target adapters, session lifecycle states, safe smoke tests, local JSON outputs, and documentation under `docs/scanner-engine.md`.

Phase 5 does not implement a real attack prompt library, evaluator logic, backend scan APIs, public scan execution, auth, dashboard integration, database persistence, billing, queue workers, PDF generation, browser automation, CI integration, SSRF protection, or target ownership verification.

## Phase 6: Prompt Library

Status: completed

Created a versioned attack prompt/test-case library under `packages/prompt_library`. It includes a manifest, schema reference, category-based JSON files, 88 safe V0 test cases, loader utilities, validation utilities, and documentation under `docs/prompt-library.md`.

Phase 6 does not implement evaluator logic, LLM-as-judge behavior, vulnerability scoring, backend scan APIs, public scan execution, auth, dashboard integration, database persistence, billing, queue workers, PDF generation, browser automation, target ownership verification, SSRF protection, or report generation.

## Phase 7: Evaluator System

Status: completed

Created a deterministic stdlib-only evaluator system under `packages/evaluator_system`. It classifies Phase 5 scanner observations with Phase 6 prompt metadata into structured verdicts, severities, confidence values, evidence snippets, redacted evidence, reasoning summaries, and manual-review flags.

Phase 7 does not implement LLM-as-judge behavior, complex ML classifiers, backend scan APIs, public scan execution, auth, dashboard integration, database persistence, billing, queue workers, PDF generation, browser automation, target ownership verification, SSRF protection, or report generation.

## Phase 8: Manual Audit Workflow

Status: completed

Created Sherlock's manual and semi-automated audit workflow under `docs/audits` with lightweight templates under `templates`. The workflow defines how real client audits can be run before a full self-serve SaaS platform exists.

Implemented as documentation and templates only:

- client intake workflow
- authorization and permission rules
- reusable audit scope template
- manual audit checklist
- category-specific safe manual testing playbooks
- evidence handling workflow
- finding review workflow
- severity and confidence review guidance
- report delivery workflow
- retest workflow
- audit closure workflow
- lightweight templates for intake, scope, finding review, retest records, and closure

Phase 8 does not implement backend APIs, database persistence, auth, billing, dashboard integration, queue workers, PDF generation, report generation code, public scan execution, admin panel, destructive testing automation, unauthorized target scanning, or exploit automation.

## Phase 9: Backend API Foundation

Status: completed

Created the first backend API foundation under `apps/api` using a minimal FastAPI structure that matches Sherlock's existing Python package direction.

Implemented as foundation only:

- backend API app skeleton
- health endpoint
- version/status endpoint
- placeholder route modules for projects, targets, scans, findings, reports, and verification
- shared response envelope with `success`, `data`, `error`, and `metadata`
- config loading for app name, brand, environment, API version, allowed origins placeholder, and debug flag
- structured error handling for validation, not found, not implemented, and internal errors
- basic logging setup
- CORS placeholder for local origins
- local API documentation in `apps/api/README.md`
- lightweight API foundation tests
- integration notes for future scanner, prompt library, evaluator, database, auth, dashboard, worker, findings, report, billing, and hardening phases

Phase 9 does not implement database persistence, Supabase integration, authentication, authorization, billing, dashboard integration, queue workers, background scan execution, public scan execution, target ownership verification, SSRF protection implementation, real report generation, PDF export, admin panels, or public scanner exposure.

## Phase 10: Database Setup

Status: completed

Created the database foundation for future Sherlock platform phases using plain PostgreSQL/Supabase-compatible SQL under `db/`.

Implemented as foundation only:

- root-level `db/` directory with README, schema documentation, migrations, and seed guidance
- initial migration for organizations, user profiles, organization members, projects, targets, target verifications, scans, scan events, findings, reports, manual audits, retests, usage records, and audit logs
- UUID primary keys, timestamps, foreign keys, indexes, and controlled check constraints
- RLS enabled on application tables with no permissive user policies yet
- documentation for entity relationships, local setup, migration workflow, RLS strategy, and privacy/security boundaries
- backend config placeholder for `DATABASE_URL` while keeping runtime database use disabled

Phase 10 does not implement authentication, authorization, login/signup, sessions, dashboard integration, billing, queue workers, public scan execution, scanner-to-database production integration, target ownership verification logic, real report generation, PDF export, admin panels, real customer data storage, or active API persistence.

## Phase 11: Authentication and User Accounts

Status: completed foundation

Created the authentication and user account foundation for future Sherlock product usage using Supabase Auth as the intended auth provider.

Implemented as foundation only:

- Supabase Auth-compatible architecture documentation in `docs/auth.md`
- safe auth placeholders in `.env.example`
- backend config fields for Supabase URL, anon key, server-only service-role key, JWKS URL, and auth enable flag
- FastAPI auth helper/dependency foundation under `apps/api`
- strict bearer-token extraction helper that does not trust arbitrary user IDs
- current-user, profile, and organization membership response schemas
- public `GET /api/v0/auth/status` route for auth configuration state
- protected `GET /api/v0/me` route foundation that returns auth unavailable until real auth is configured
- shared-envelope auth errors for unavailable or missing authentication
- documentation for user profiles, organizations, memberships, roles, backend token validation, and future RLS strategy
- lightweight auth helper tests

Phase 11 does not implement production login/signup UI, production JWT verification, sessions, authenticated dashboard, billing, queue workers, public scan execution, target verification, active API database persistence, scanner execution exposure, report generation, PDF export, admin panels, broad RLS policies, or real secrets.

## Phase 12: Dashboard V0 + Auth UI Shell

Status: completed foundation

Created the first product dashboard UI/UX foundation under the existing static `apps/web` implementation.

Implemented as static UI only:

- login page UI shell
- signup page UI shell
- forgot-password page UI shell
- protected dashboard layout shell
- dashboard overview page
- projects page
- scans page
- findings page
- reports page
- settings/account page
- consistent dashboard navigation, workspace/account placeholders, empty states, loading/error state patterns, status badges, and disabled future-action controls
- clear "Dashboard V0", "demo shell", and "not connected yet" messaging
- optional safe display of `GET /api/v0/auth/status` on auth/settings pages when the local API is running
- public website links to login and Dashboard V0

Phase 12 does not implement production auth/session flow, live Supabase browser integration, production JWT verification, active database persistence from the UI, real project creation, real scan creation, scanner execution, target ownership verification, queue workers, billing, generated web reports, PDF export, admin panels, or destructive testing.

## Phase 13: Project Target Setup

Status: completed foundation

Created the first project and target setup UI/UX foundation under the existing static dashboard implementation.

Implemented as static UI and placeholder contract documentation only:

- projects page setup CTA and empty-state language
- project setup page for project name, description, environment, app type, data sensitivity, framework/stack, and notes
- project detail placeholder with target section
- target setup page for safe target metadata, target type, URL, HTTP method, auth placeholder type, format notes, rate limit notes, test account notes, RAG/private-docs involvement, tools/actions involvement, and acknowledgement placeholders
- target detail placeholder
- setup progress indicator for project details, target metadata, authorization/scope, Phase 14 verification later, and Phase 15 scanning later
- disabled verify-target and run-scan actions with future-phase labels
- project/target placeholder API contract metadata documenting safe fields and forbidden secret fields
- docs updates clarifying that persistence, verification, scanning, billing, queues, findings, reports, PDF generation, and admin surfaces remain future work

Phase 13 does not implement real production project persistence, target persistence from the UI, active API database persistence, production auth/session flow, target ownership verification, DNS/meta/file verification logic, scanner execution, public scanning, queue workers, billing, findings persistence, generated reports, PDF export, admin panels, destructive testing, service-role usage in frontend, or real secret storage.

## Phase 14: Target Ownership Verification

Status: completed foundation

Establish the target ownership verification foundation. Verification proves that a user controls or is authorized to test a target before any scan can run.

Implemented:

- verification method definitions: DNS TXT record, HTML meta tag, well-known file, manual authorization review, chatbot/API challenge
- verification status lifecycle: unverified, pending, verified, failed, expired, manual_review_required
- challenge token format design: `sherlock_<random_urlsafe_token>` with SHA-256 hashing, expiry, and scoping
- API contract placeholders in `apps/api/app/schemas/verification.py` (method registry, status registry, challenge token design, request/response contracts)
- safe validation helpers in `apps/api/app/verification.py` (token generation, hashing, format checks — no network requests)
- `GET /api/v0/verification` route returns full Phase 14 contract as structured 501 details
- `apps/web/dashboard/target-verification.html` — verification page with method selector, instructions per method, status card, history placeholder, and security boundaries
- updated target detail, target setup, project detail, projects, and dashboard overview pages with Phase 14 verification links and status
- unit tests for verification helpers and API contract
- `docs/verification.md` — comprehensive verification documentation
- docs updates to roadmap, architecture, development, security, web README, and API README

Phase 14 does not implement production DNS/HTTP/chatbot verification checks, active API persistence of verification records, SSRF-safe network requests, rate-limited verification attempts, scan unlocking, scanner execution, queue workers, billing, findings, generated reports, PDF export, admin panels, destructive testing, service-role usage in frontend, or real secret storage.

## Phase 15: Queue + Worker System

Status: completed foundation

Created the queue and worker system foundation under `packages/worker_system`. This phase prepares Sherlock to run future scans asynchronously through background workers.

Implemented as foundation only:

- queue abstraction with `QueueBackend` interface and `LocalMemoryQueue` in-memory dev backend
- job payload and result schemas (JSON-serializable, no secrets)
- four job types: `scan.run`, `scan.evaluate`, `scan.summarize`, `report.prepare_placeholder`
- eight lifecycle states: `queued`, `running`, `completed`, `failed`, `cancelled`, `timed_out`, `blocked_unverified`, `blocked_unsafe`
- safety gates: queue enabled, target verified, job type allowed, target URL safe, no secrets in payload, limits enforcement
- worker engine with mock scan execution via Phase 5 `MockTargetAdapter` only
- local worker CLI for safe dry-runs
- queue/worker contract metadata on the scans API placeholder route
- dashboard queue status messaging and lifecycle reference
- worker system unit tests
- documentation in `docs/workers.md`
- `.env.example` placeholders for `QUEUE_BACKEND`, `WORKER_ENABLED`, `WORKER_MAX_CONCURRENT_JOBS`, `WORKER_JOB_TIMEOUT_SECONDS`, `SCAN_MAX_TESTS_PER_JOB`
- `worker-output/` and `worker-results/` added to `.gitignore`

Phase 15 does not implement public scan execution, production queue deployment, real network scanning, production DNS/HTTP/chatbot verification checks, billing, findings persistence, report generation, PDF export, admin panels, service-role usage in frontend, real secret storage, or broad RLS policies.

## Phase 16: Scan Types + Limits

Status: completed foundation

Created Sherlock's scan type and limit system foundation under `packages/scan_limits`. This phase defines safe scan modes, plan-aware limits, category inclusion rules, worker job constraints, and validation helpers.

Implemented:

- five scan type definitions: quick_scan, standard_scan, deep_scan, manual_audit_assisted, retest_scan
- scan type configuration with max_tests, timeout_seconds, max_concurrency, response/prompt char limits, and report levels
- category registry mapped to Phase 6 prompt library categories
- per-scan-type category inclusion/exclusion matrix
- five plan/tier placeholder definitions: free, launch_scan, builder, startup, manual_audit
- plan/tier availability matrix for scan types, monthly scans, projects, retests, and export features
- composable validation helpers for scan type, categories, tests, timeout, concurrency, verification, manual audit guards, retest restrictions, and payload secret rejection
- worker system safety gate integration with backward-compatible scan_type_limits gate
- API GET /api/v0/scans/types and GET /api/v0/scans/limits endpoints with static scan type and limit metadata
- dashboard scan setup page with scan type cards, limit details, plan tier table, and disabled run buttons
- 82 unit tests covering all scan types, limits, categories, plans, and validators
- environment placeholders for SCAN_LIMITS_ENABLED, DEFAULT_SCAN_TYPE, MAX_SCAN_TESTS_PER_JOB, MAX_SCAN_TIMEOUT_SECONDS, MAX_SCAN_CONCURRENCY, FREE_TIER_MONTHLY_SCANS, DEEP_SCAN_ENABLED
- comprehensive documentation in docs/scan-types-and-limits.md

Phase 16 does not implement public scan execution, billing, Stripe, PDF/report generation, admin panels, production queue deployment, findings persistence, real network scanning, service-role usage in frontend, real secret storage, or broad RLS policies.

## Phase 17: Findings System

Status: completed foundation

Created Sherlock's findings system foundation under `packages/findings_system`. This phase converts safe/mock evaluator output into structured finding candidates and finalized finding objects that are clear enough for non-security developers and ready for future report consumption.

Implemented:

- finding candidate model for evaluator-derived observations
- finalized finding model with title, category, severity, confidence, status, description, business impact, evidence, reproduction steps, fix recommendation, source IDs, evaluator signals, duplicate group key, manual review placeholders, timestamps, and metadata
- normalized statuses: `open`, `fixed`, `accepted_risk`, `false_positive`, `needs_review`
- severity and confidence validation aligned to the methodology
- category mapping across methodology, prompt library, scan limits, and evaluator signal names
- duplicate grouping and similar finding merge helpers
- sorting by severity, confidence, category, and title
- redacted evidence summary helpers
- fix recommendation templates by category
- adapter from Phase 7 evaluator output to finding candidates
- local CLI for safe/mock evaluator JSON conversion
- API `GET /api/v0/findings/schema` static metadata endpoint
- static dashboard findings page updated with Phase 17 structure and statuses
- tests for validation, grouping, merging, sorting, category mapping, recommendations, evaluator adapter, and evidence redaction
- documentation in `docs/findings-system.md`

Phase 17 does not implement Phase 18 web reports, report generation, PDF export, public scan execution, production dashboard API integration, active findings persistence, real database writes, billing, Stripe, admin panels, real network scanning, LLM-as-judge, or real customer evidence storage.

## Phase 18: Web Report

Status: completed foundation

Created Sherlock's web report foundation under `packages/report_system` and the static dashboard report shell under `apps/web/dashboard/report-detail.html`.

Implemented:

- structured report model with report status, report type, launch readiness verdict, score, summary, severity breakdown, top fixes, findings, tested categories, not-tested scope, limitations, evidence handling note, retest status, methodology version, findings system version, source scan ID, and metadata
- normalized report statuses: `draft`, `ready`, `needs_review`, `archived`
- normalized report types: `web`, `sample`, `manual_audit`, `scan_summary`
- careful verdicts: `ready_with_low_risk`, `needs_fixes_before_launch`, `high_risk_do_not_launch`, `manual_review_required`, `inconclusive`
- conservative bounded score helper
- severity breakdown, top fixes, findings table shaping, tested category formatting, limitations, and redacted evidence helpers
- builder from explicit Phase 17 finding objects and sanitized/static metadata
- report system unit tests
- API `GET /api/v0/reports/schema` static report contract metadata
- dashboard reports page and report detail shell using demo/static data only
- documentation in `docs/web-report.md`

Phase 18 does not implement PDF export, downloadable reports, billing, paid gates, public scan execution, scanner execution from public UI/API, production queue deployment, active database persistence, report database writes, real report sharing tokens, public report links with access control, admin panels, real customer evidence storage, raw sensitive evidence storage, real network scanning, or report generation from real customer scans.

## Phase 19: PDF Report Export

Status: completed foundation

Created Sherlock's PDF report export foundation under `packages/pdf_export`, extending the Phase 18 report object with a PDF-ready export contract, safety checks, and a dependency-light print-ready HTML template.

Implemented:

- PDF export data model with cover page, executive summary, verdict, score, severity breakdown, top fixes, findings table, detailed findings, evidence snippets, reproduction steps, fix recommendations, tested categories, not-tested scope, limitations, evidence handling note, footer disclaimer, source report ID, and metadata
- normalized export statuses: `draft`, `ready`, `blocked_sensitive_evidence`, `failed`, `archived`
- export types: `pdf`, `print_html`, `preview`
- builder from Phase 18 `Report` objects
- print-ready HTML renderer for local/demo browser print-to-PDF use
- local/demo CLI for schema/demo inspection and optional ignored HTML artifact generation
- safe filename and output path validation for `pdf-output/`, `pdf-exports/`, and `report-exports/`
- evidence redaction/safety validation and overclaiming verdict rejection
- API `GET /api/v0/reports/schema` extended with static PDF export contract metadata
- dashboard report detail placeholder button for the Phase 19 PDF export foundation
- documentation in `docs/pdf-export.md`

Phase 19 does not implement production PDF export for real customer reports, public PDF download links, public report sharing, billing, Stripe, live paid-plan gates, active report database persistence, report database writes, production storage integration, email delivery, admin panel, real customer evidence storage, public scan execution, scanner execution from public UI/API, real network scanning, or Phase 20 retest flow.

## Phase 20+: Product Platform

Future platform work may include:

- Phase 20 retest flow
- Phase 21 billing callbacks
- Phase 22 security hardening, SSRF protection, rate limits, observability, and audit logging
- production DNS/HTTP/chatbot verification backend checks
- active API persistence of verification records
- challenge token TTL enforcement
- manual authorization file upload and admin review
- production Redis/RQ queue backend
- productized retest management
- local runner
- GitHub/CI integration
- compliance mapping
