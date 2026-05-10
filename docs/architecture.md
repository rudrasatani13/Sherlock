# Architecture Vision

Sherlock is planned as a modular AI launch security audit and scanner platform. The architecture should keep customer-facing workflows, scan execution, prompt libraries, evaluators, reports, and billing separated so each area can evolve without becoming tightly coupled.

This document describes the future direction and the current Phase 19 PDF export foundation. Phase 17 adds structured finding candidates, finalized finding models, category/status/severity/confidence alignment, evaluator adapters, grouping, merging, sorting, redacted evidence summaries, and recommendation templates under `packages/findings_system`. Phase 18 adds structured report models, conservative scoring, careful launch-readiness verdicts, section shaping, limitations, report-appropriate evidence formatting, static report schema metadata, and a static dashboard web report shell. Phase 19 adds a PDF export contract, print-ready HTML renderer, safety checks, local/demo CLI, static PDF export metadata, and disabled dashboard export placeholder under `packages/pdf_export`. It builds on Phase 16 scan limits, Phase 15 queue/worker, Phase 14 verification, Phase 13 setup, Phase 12 dashboard, Phase 11 auth, Phase 10 database, Phase 9 API, and Phase 7 evaluator foundations. It does not implement public scan execution, billing, Stripe, public PDF downloads, production PDF delivery, admin panels, production queue deployment, active findings persistence, active report persistence, production storage integration, or real network scanning.

## Planned Components

### Web App, Dashboard, and Public Website

The future web app will cover the public website, authenticated dashboard, scan setup flows, report viewing, team/account settings, and billing surfaces.

Phase 2 implements the public website as a static site under `apps/web`. Phase 12 keeps that static approach and adds login, signup, forgot-password, dashboard overview, projects, scans, findings, reports, and settings pages as a Dashboard V0 shell. Phase 13 extends the same static approach with project setup, target setup, project detail placeholder, and target detail placeholder pages. Phase 14 adds a target ownership verification page with method selection, challenge instructions, verification status, and security boundaries.

The Phase 14 dashboard verification flow is UI only. It uses static/demo data, browser-only method switching, disabled verification submission, and links to the verification page from target and project detail pages. It does not create sessions, trust fake users, persist verification records, issue real challenges, perform DNS/HTTP/chatbot checks, store secrets, run scans, generate findings, generate reports, or handle billing.

Phase 4 expands the static public sample report page. It is a demo-only artifact, not a real customer report viewer and not generated from a scan. Phase 18 adds a static dashboard report detail shell that previews the future web report structure using demo data only. Phase 19 adds a disabled PDF export foundation control to the report detail shell; it does not create a production customer download.

### Methodology and Finding Taxonomy

The Phase 3 methodology is documented in `docs/methodology.md`. It defines the vulnerability categories, evidence standards, severity model, confidence model, finding statuses, report language standards, and future implementation guidance.

The methodology should remain separate from executable scanner logic, prompt text, evaluator code, and report rendering. Future implementation phases should reference the methodology rather than duplicating taxonomy rules in scattered code or page copy.

### Backend API

The backend API will eventually handle scan configuration, account data, report access, billing webhooks, target verification, and integration endpoints. API boundaries should be designed around explicit contracts and should avoid leaking scanner internals into UI code.

Phase 9 adds `apps/api`, a small FastAPI foundation with:

- `GET /health` for runtime health
- `GET /version` for phase/module status
- `GET /api/v0/auth/status` for Phase 11 auth configuration status
- `GET /api/v0/me` as a protected current-user route foundation
- placeholder `501 not_implemented` route groups for projects, targets, scans, findings, reports, and verification
- Phase 13 project/target setup contract metadata on the placeholder projects and targets routes
- Phase 14 verification contract with method registry, status definitions, challenge token design, and request/response schemas on the verification route
- safe verification helpers (token generation, hashing, format checks — no network requests)
- `GET /api/v0/reports/schema` for static Phase 18 report contract metadata and Phase 19 PDF export contract metadata
- shared response envelope, config loading, logging, CORS placeholder, and structured error handling

The API does not persist data through routes, run production JWT verification, create projects or targets, create verification challenges, perform DNS/HTTP/chatbot verification checks, create scans, call the scanner engine, generate reports from real scans, return customer reports, create share links, create public PDF downloads, handle billing, or start workers. Scanner execution must remain isolated until future phases add production authentication, authorization, production verification checks, SSRF protection, rate limits, spend controls, audit logging, and queue workers.

Phase 12, Phase 13, and Phase 14 web pages may read `GET /api/v0/auth/status` when the local API is running, but no browser token, service-role key, protected API route, project persistence route, target persistence route, verification persistence route, or scanner route is used by the dashboard shell.

### Scanner Engine

The scanner engine coordinates controlled internal test execution against authorized AI targets. It remains isolated from presentation code and exposes clear inputs, outputs, limits, and failure states.

Phase 5 adds `packages/scanner_engine`, a stdlib-only internal Python package with scan config validation, session lifecycle states, target adapters, safe smoke tests, local JSON outputs, and extension points for later prompt library and evaluator phases.

The Phase 5 scanner is not exposed through the public website, backend APIs, dashboard, or customer-facing scan flows.

### Prompt Suite

The prompt suite contains versioned test prompts and scenario definitions. It should support careful review, provenance, and change tracking because prompt changes can alter findings and report interpretation.

Phase 6 adds `packages/prompt_library`, a stdlib-only internal attack prompt/test-case library with a manifest, schema reference, category files, safe metadata, loader utilities, validation utilities, and scanner conversion helpers. The Phase 5 scanner still defaults to benign smoke test fixtures and does not automatically execute the attack prompt library.

### Evaluator System

The evaluator system classifies captured model behavior into structured local evaluation results. It is versioned separately from prompts and scanner orchestration.

Phase 7 adds `packages/evaluator_system`, a stdlib-only deterministic evaluator package with rule-based detectors, result schemas, evidence redaction helpers, a local CLI, and unittest coverage. It consumes Phase 5 scanner observations and Phase 6 prompt metadata when present.

### Findings System

The findings system converts evaluator/scanner observations into clean, actionable finding candidates and finalized finding objects. It sits between evaluator output and future reports so report rendering does not need to know detector internals.

Phase 17 adds `packages/findings_system`, a stdlib-only internal package with:

- normalized finding statuses: `open`, `fixed`, `accepted_risk`, `false_positive`, and `needs_review`
- normalized severities and confidences from the methodology
- category mapping across methodology, prompt library, scan limits, and evaluator signal names
- finding candidate and finalized finding dataclasses
- validator rules for evidence, fix guidance, critical severity, status, and vague language
- evaluator-output-to-candidate adapter
- duplicate grouping and similar finding merge helpers
- severity/confidence/category/title sorting
- redacted evidence summaries for report use
- category recommendation templates
- local CLI for safe/mock evaluator JSON conversion

Phase 17 is not a persistence layer. It does not write to the Phase 10 `findings` table, store raw evidence, generate reports, export PDFs, or connect the dashboard to production findings.

### Manual Audit Workflow

The manual audit workflow turns intake, authorization, scanner observations, prompt-library scenarios, evaluator outputs, manual validation, evidence handling, finding review, delivery, retesting, and closure into a repeatable human-led process.

Phase 8 adds documentation under `docs/audits` and lightweight templates under `templates`. It is a process layer only and does not add backend APIs, persistence, dashboard screens, report generation, PDF export, admin review panels, queue workers, billing, auth, public scan execution, or destructive testing automation.

### Async Scan Workers

Long-running scans run outside request/response paths through workers and queues. The worker layer enforces timeouts, concurrency limits, retry policy, spend limits, and cancellation.

Phase 15 adds `packages/worker_system` with:

- `QueueBackend` abstraction and `LocalMemoryQueue` in-memory dev backend
- job payload and result schemas (JSON-serializable, no secrets)
- job types: `scan.run`, `scan.evaluate`, `scan.summarize`, `report.prepare_placeholder`
- lifecycle states: queued, running, completed, failed, cancelled, timed_out, blocked_unverified, blocked_unsafe
- safety gates: target verified, URL safe, no secrets, limits enforcement
- worker engine with Phase 5 MockTargetAdapter mock scan execution
- local worker CLI for dry-runs

The Phase 15 worker is local/mock only. Production queue deployment requires Redis/RQ or Celery backend, production auth, target verification, SSRF protection, and rate limits.

### Scan Types and Limits

The scan limits system ensures every scan mode has bounded test counts, timeouts, concurrency, category rules, and verification requirements.

Phase 16 adds `packages/scan_limits` with:

- Five scan type definitions: quick_scan, standard_scan, deep_scan, manual_audit_assisted, retest_scan
- Bounded limits per scan type (max_tests, timeout, concurrency, response/prompt char limits)
- Category inclusion/exclusion matrix mapped to Phase 6 prompt library
- Five plan/tier placeholders: free, launch_scan, builder, startup, manual_audit
- Composable validation helpers for all limit enforcement
- Worker system safety gate integration (`scan_type_limits` gate)
- API endpoints: `GET /api/v0/scans/types` and `GET /api/v0/scans/limits`
- Dashboard scan setup page with type cards and disabled run buttons

The Phase 16 scan limits are static configuration. Dynamic overrides from database, admin, or billing integration are future work.

### Database and Auth

The database will eventually store accounts, users, scan configurations, ownership verification state, scan runs, findings, report metadata, billing state, and audit logs.

Phase 10 adds a root-level `db/` foundation using plain PostgreSQL/Supabase-compatible SQL migrations and documentation. The initial schema covers organizations, user profiles, organization members, projects, targets, target verifications, scans, scan events, findings, reports, manual audits, retests, usage records, and audit logs.

Phase 11 selects Supabase Auth as the intended identity provider and adds the backend auth foundation under `apps/api`. Supabase Auth stores users in the managed `auth` schema; Sherlock app-level metadata should live in `public.user_profiles`, `public.organizations`, and `public.organization_members`.

The Phase 10 migration enables RLS on application tables but does not add permissive user policies. Phase 11 keeps that deny-by-default posture, and Phases 12 and 13 do not change it. Future RLS policies should use `auth.uid()` and organization membership rows to enforce tenant boundaries after production JWT validation and real dashboard persistence flows are reviewed.

The Phase 13 target setup UI supports generic labels such as RAG application and tool-using agent. Before active persistence is enabled, the project/target API contract and Phase 10 `target_type` enum should be reconciled through a reviewed migration or explicit mapping.

The service-role key is server-only and must never be exposed to browser/frontend code.

### Report System

Reports present evidence, severity, reproduction context, limitations, and remediation guidance. Reports must redact sensitive data and must avoid claiming that a target is fully secure.

Phase 18 adds `packages/report_system`, a stdlib-only internal package with:

- normalized report statuses: `draft`, `ready`, `needs_review`, and `archived`
- report types: `web`, `sample`, `manual_audit`, and `scan_summary`
- launch readiness verdicts that avoid "secure", "safe", "certified", and "guaranteed" wording
- a conservative bounded security score helper
- severity breakdown, top fixes, findings table, tested categories, limitations, and evidence formatting helpers
- a builder that accepts explicit sanitized/static Phase 17 finding objects and metadata
- static API schema metadata at `GET /api/v0/reports/schema`
- a static dashboard web report shell under `apps/web/dashboard/report-detail.html`

Reports should follow the severity, confidence, finding status, evidence, and language standards in `docs/methodology.md`, and should consume reviewed finding objects from `packages/findings_system` rather than raw evaluator detector output.

The Phase 4 sample report reference in `docs/sample-report.md` documents a static content structure and fictional demo findings. It is not executable schema, report generation logic, a persistence model, or a PDF export system.

The Phase 8 report delivery workflow in `docs/audits/REPORT_DELIVERY.md` describes how an auditor can manually prepare and deliver a scoped report before report generation exists.

Phase 18 is not a persistence layer. It does not write to the Phase 10 `reports` table, generate PDFs, create download assets, create real public share links, enforce billing gates, read real scan outputs by default, store raw evidence, or return customer reports through the API.

Generated reports should not be committed to the repository.

### PDF Export

Phase 19 adds `packages/pdf_export`, a stdlib-only internal package with:

- normalized export statuses: `draft`, `ready`, `blocked_sensitive_evidence`, `failed`, and `archived`
- export types: `pdf`, `print_html`, and `preview`
- PDF export data contracts for cover page, executive summary, verdict, score, severity breakdown, top fixes, findings table, detailed findings, evidence snippets, reproduction steps, fix recommendations, tested categories, not-tested scope, limitations, evidence handling note, footer disclaimer, source report ID, and metadata
- a builder that accepts Phase 18 `Report` objects
- print-ready HTML rendering for local/demo browser print-to-PDF use
- safety checks for redacted evidence, overclaiming verdicts, limitations, safe filenames, and output path boundaries
- local/demo CLI support that defaults to stdout and writes only to ignored artifact directories when explicitly requested

The Phase 19 package is not a production delivery system. It does not create public download URLs, store customer PDFs, write report database records, enforce paid plans, send email, expose customer evidence, or implement Phase 20 retesting.

Local generated export artifacts must stay in ignored directories such as `pdf-output/`, `pdf-exports/`, or `report-exports/`.

### Billing

Billing should be added after the core audit workflow and report value are proven. Billing events must be handled server-side and verified before granting usage.

### Local Runner

A local runner may eventually support customer-controlled testing against private environments. It should minimize data transfer, clearly explain what leaves the customer's environment, and avoid unsafe default network reachability.

### GitHub and CI Integration

Future GitHub/CI integration may allow teams to run approved checks before launch. It should use explicit target verification, scoped credentials, safe logging, and clear failure behavior.

## Repository Direction

The current foundation uses:

- `apps/` for future deployable applications
- `apps/api` for the Phase 9 backend API foundation with Phase 13 setup contracts, Phase 14 verification contracts, and Phase 15 queue/worker contracts
- `apps/web` for the static public website and dashboard/auth/project-target setup/verification UI shell
- `db/` for the Phase 10 PostgreSQL/Supabase-compatible database foundation
- `packages/` for future shared libraries and core domain modules
- `config/` for shared product metadata and future configuration
- `docs/` for product, architecture, setup, roadmap, security, and scope notes

Phase 16 adds a scan type and limit system under `packages/scan_limits` with bounded scan modes, category inclusion rules, plan tier placeholders, and validation helpers. Phase 17 adds `packages/findings_system` for structured findings and safe metadata contracts. Phase 18 adds `packages/report_system` for structured web report contracts and a static dashboard report shell. Phase 19 adds `packages/pdf_export` for PDF export contracts, safety checks, and print-ready HTML rendering. The project should stay minimal until a real implementation phase needs a new framework, package manager, active persistence layer, production queue, storage service, or deployment target.
