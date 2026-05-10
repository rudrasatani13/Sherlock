# Scope Boundaries

`SHERLOCK_DEVELOPMENT_MASTER_PLAN.md` is the long-term reference. The current implementation provides **foundation versions** through Phase 19. It does not provide full production-complete versions. See [Master Plan Alignment](master-plan-alignment.md) for more context.

Sherlock has completed Phase 19 PDF Report Export foundation.

## In Scope for Phase 1

- repository organization
- documentation
- environment templates
- development notes
- security notes
- roadmap notes
- basic ignore/config files
- simple product metadata
- future-facing placeholder directories with explanations

## In Scope for Phase 2

- static public website under `apps/web`
- homepage and product positioning
- sample report page with demo-only content
- public methodology page
- security/trust page
- pricing and early-access page
- contact, beta, and audit request UI
- shared static styling and frontend-only navigation/form behavior
- SEO metadata for public pages

## In Scope for Phase 3

- detailed internal methodology documentation
- vulnerability category definitions
- evidence requirements
- severity system
- confidence system
- finding status definitions
- report language standards
- future implementation guidance for prompt library, evaluator rules, scanner engine, findings model, report generator, and manual audit workflow
- public methodology page refinement

## In Scope for Phase 4

- polished static public sample report page
- clearly labeled sample/demo report content
- fictional target app and demo findings
- sanitized evidence examples
- launch readiness verdict and sample security score
- severity, confidence, status, and retest language aligned to the methodology
- tested and not-tested scope language
- limitations, disclaimer, and final recommendation language
- internal sample report reference documentation

## In Scope for Phase 5

- internal scanner engine package under `packages/scanner_engine`
- scan configuration format
- target adapter abstraction
- mock target adapter for local dry-runs
- generic HTTP/API target adapter for authorized internal testing
- safe smoke test fixtures only
- scan session lifecycle states
- local JSON raw result, structured result, and summary outputs
- scanner engine documentation

## In Scope for Phase 6

- internal attack prompt/test-case library under `packages/prompt_library`
- versioned prompt library manifest
- prompt/test-case schema reference
- category-based JSON prompt files
- safe metadata for expected behavior and failure signals
- fake/demo context setup examples
- prompt library loader utilities
- prompt library validation utilities
- scanner conversion helper for the Phase 5 `ScannerTest` shape
- prompt library documentation

## In Scope for Phase 7

- internal evaluator system package under `packages/evaluator_system`
- deterministic rule-based detectors
- structured evaluation result types
- evidence snippet extraction
- redacted evidence helpers
- canary token leakage detection using fake/demo metadata
- sensitive data pattern detection
- system prompt leakage detection
- unsafe output detection
- tool/function abuse detection
- cost abuse detection
- manual review flags and reasons
- local evaluator CLI for scanner result JSON files
- evaluator documentation
- unittest coverage

## In Scope for Phase 8

- manual audit workflow documentation under `docs/audits`
- client intake workflow
- authorization and permission rules
- audit scope template
- manual audit checklist
- category-specific safe manual testing playbooks
- evidence handling workflow
- finding review workflow
- severity and confidence review workflow
- report delivery workflow
- retest workflow
- audit closure workflow
- lightweight markdown templates under `templates`

## In Scope for Phase 9

- backend API app skeleton under `apps/api`
- FastAPI health endpoint
- FastAPI version/status endpoint
- placeholder route modules for projects, targets, scans, findings, reports, and verification
- shared response envelope
- request/response schema foundation
- app config/loading
- structured error handling
- basic logging setup
- CORS config placeholder
- local development docs
- API docs explaining future route groups
- lightweight API foundation tests
- safe integration notes for future scanner, prompt library, and evaluator use

## In Scope for Phase 10

- root-level database foundation under `db/`
- PostgreSQL/Supabase-compatible SQL migration structure
- initial schema for organizations, user profiles, memberships, projects, targets, target verifications, scans, scan events, findings, reports, manual audits, retests, usage records, and audit logs
- schema documentation and entity relationship notes
- local database setup guidance
- RLS and access-control planning
- safe backend database config placeholder only
- documentation updates explaining future database integration boundaries

## In Scope for Phase 11

- Supabase Auth-compatible architecture documentation
- safe auth environment placeholders
- backend auth helper/dependency foundation
- strict bearer-token extraction helper
- current-user model/schema foundation
- public auth configuration status route
- protected current-user route placeholder
- shared-envelope auth error style
- user profile, organization, membership, and role model documentation
- future JWT validation and RLS strategy documentation
- local development behavior without real Supabase credentials
- auth helper tests

## In Scope for Phase 12

- static login UI shell
- static signup UI shell
- static forgot-password UI shell
- protected dashboard layout shell
- dashboard overview, projects, scans, findings, reports, and settings pages
- consistent dashboard navigation, workspace/account placeholders, empty states, loading/error patterns, status badges, and disabled future actions
- static/demo dashboard data clearly labeled as demo-only
- optional frontend display of the safe `GET /api/v0/auth/status` endpoint when the local API is running
- documentation updates for dashboard/auth UI boundaries

## In Scope for Phase 13

- projects page empty state and setup CTA
- static project setup page for project name, description, environment, app type, data sensitivity, framework/stack, and notes
- static project detail placeholder with target section
- static target setup page for target name, target type, URL, HTTP method, auth placeholder type, request/response notes, rate limit notes, test account notes, RAG/private-docs involvement, tools/actions involvement, production-impact acknowledgement, and authorization/scope acknowledgement
- static target detail placeholder
- target type selector for API endpoint, OpenAI-compatible endpoint, Vercel AI SDK endpoint, RAG application, tool-using agent, chatbot URL, and manual audit target
- browser-only form validation and local setup preview
- setup progress indicator covering project details, target metadata, authorization/scope, Phase 14 verification later, and Phase 15 scanning later
- disabled verify-target and run-scan actions with future-phase labels
- project and target placeholder API contract metadata documenting safe fields and forbidden secret fields
- documentation updates for project/target setup boundaries

## In Scope for Phase 14

- target ownership verification foundation
- verification method definitions (DNS TXT, HTML meta tag, well-known file, manual authorization, chatbot/API challenge)
- challenge token design
- safe validation helpers
- target ownership verification UI shell
- Phase 14 verification contract placeholder on the API

## In Scope for Phase 15

- queue and worker system foundation
- job schemas
- safety gates
- local worker engine with mock scan execution
- worker CLI

## In Scope for Phase 16

- scan types, limits, category matrix, plan placeholders, validation helpers, static API metadata, dashboard scan setup shell, and worker safety-gate integration

## In Scope for Phase 17

- findings system package under `packages/findings_system`
- finding candidate and finalized finding models
- normalized finding statuses, severities, confidences, and category mapping
- evaluator-output-to-finding-candidate adapter
- duplicate grouping, similar merge, and severity/confidence sorting helpers
- redacted evidence summary helpers
- reproduction-step formatting helpers
- category recommendation templates
- manual review note placeholders
- local CLI for safe/mock evaluator output conversion
- unit tests for validation, grouping, sorting, merge behavior, recommendations, category mapping, evaluator adapter, and evidence redaction
- static API findings schema metadata endpoint
- static dashboard findings page copy aligned to Phase 17
- documentation updates

## In Scope for Phase 18

- report system package under `packages/report_system`
- structured report object model
- normalized report statuses: `draft`, `ready`, `needs_review`, `archived`
- normalized report types: `web`, `sample`, `manual_audit`, `scan_summary`
- careful launch readiness verdict helpers without overclaiming language
- conservative 0-100 score helper
- severity breakdown helper
- top fixes helper
- findings table data shaping
- detailed report finding shaping
- tested categories formatting
- limitations helper
- report-appropriate evidence formatting using Phase 17 redaction helpers
- builder from explicit sanitized/static Phase 17 finding objects
- static dashboard report list update
- static dashboard report detail shell
- API `GET /api/v0/reports/schema` static metadata endpoint
- report system unit tests
- documentation updates

## In Scope for Phase 19

- PDF export package under `packages/pdf_export`
- PDF export data contract
- normalized export statuses: `draft`, `ready`, `blocked_sensitive_evidence`, `failed`, `archived`
- export types: `pdf`, `print_html`, `preview`
- PDF template model
- print-ready HTML renderer for local/demo browser print-to-PDF use
- local/demo CLI that defaults to stdout
- optional local ignored HTML artifact output
- safe filename generation
- path traversal rejection
- output directory safety for `pdf-output/`, `pdf-exports/`, and `report-exports/`
- PDF-safe evidence validation
- section builder from Phase 18 `Report` objects
- cover page structure
- executive summary, verdict, score, severity breakdown, top fixes, findings table, detailed findings, tested categories, not-tested scope, limitations, evidence handling note, and retest status placeholder
- future secure storage and paid-plan gating notes
- disabled dashboard PDF export placeholder
- static PDF export contract metadata on `GET /api/v0/reports/schema`
- tests for model validation, statuses, filenames, path safety, evidence safety, overclaiming, limitations, template generation, report integration, CLI dry-run behavior, and output safety
- documentation updates

## Out of Scope Through Phase 19

- production login/signup/session flow
- production JWT verification
- live Supabase browser integration
- real authenticated dashboard API consumption
- dashboard database reads/writes
- real production project persistence
- target persistence from the UI
- admin panel
- billing
- production queue workers
- production PDF delivery and public PDF download links
- real customer report retrieval APIs
- active report persistence
- report database writes
- real report sharing tokens
- public report links with access control
- active API database persistence
- target verification logic
- DNS/meta/file verification logic
- real target secret storage
- public scanner execution API
- public scan execution
- production deployment configuration
- real customer data storage or handling
- real customer evidence storage
- active findings database reads or writes
- production findings dashboard integration
- production report dashboard integration
- report generation from real customer scans
- LLM-as-judge behavior
- complex ML classifiers
- browser automation scanner
- CI/GitHub integration
- destructive testing automation
- unauthorized target scanning
- public self-serve scan feature
- production PDF export for real customer reports
- public PDF download links
- public report sharing
- billing or Stripe
- live paid-plan gates
- production storage integration
- email delivery
- Phase 20 retest flow

## Naming Rules

- Repository name: Sherlock
- Product name: Sherlock
- Brand/company identity: PowerDetect
- Full marketing name: PowerDetect Sherlock

Do not rename the repository or root folder.

## Phase Gate

Phase 19 establishes the PDF export foundation required before production report delivery workflows. Future phases should use `docs/methodology.md` as the source of truth for category, evidence, severity, confidence, status, and reporting rules, `docs/findings-system.md` as the Phase 17 findings contract reference, `docs/web-report.md` as the Phase 18 web report contract reference, `docs/pdf-export.md` as the Phase 19 PDF export contract reference, `docs/sample-report.md` as a non-executable reference for report content structure, `docs/scanner-engine.md` as the scanner architecture reference, `docs/prompt-library.md` as the prompt library format reference, `docs/evaluator-system.md` as the evaluator contract reference, `docs/audits/README.md` as the manual audit workflow reference, `docs/auth.md` as the auth/account foundation reference, `apps/api/README.md` as the API foundation reference, `db/schema.md` as the database foundation reference, `docs/verification.md` for verification methods, `docs/workers.md` for the queue/worker design, and `docs/scan-types-and-limits.md` for execution bounds.
