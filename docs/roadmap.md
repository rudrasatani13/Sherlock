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

## Phase 9+: Product Platform

Future platform work may include:

- backend API
- database schema and migrations
- authentication and authorization
- dashboard
- async workers and queues
- report generation
- PDF export
- billing
- productized retest management
- target ownership verification
- SSRF protection and network controls
- local runner
- GitHub/CI integration
- observability
- security hardening
- compliance and audit logging
