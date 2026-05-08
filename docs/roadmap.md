# Roadmap

This roadmap is directional. It should guide sequencing without forcing premature architecture decisions.

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

Status: completed

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

Status: completed

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

## Phase 13+: Product Platform

Future platform work may include:

- Phase 13 project setup and safe dashboard API consumption
- Phase 14 target ownership verification
- Phase 15 async workers and queues
- Phase 17 findings system
- Phase 18 web report
- Phase 21 billing callbacks
- Phase 22 security hardening, SSRF protection, rate limits, observability, and audit logging
- productized retest management
- local runner
- GitHub/CI integration
- compliance mapping
