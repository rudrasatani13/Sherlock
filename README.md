# Sherlock

Sherlock is an AI Launch Security Audit + Scanner product under the PowerDetect brand.

The full marketing name is **PowerDetect Sherlock**. Sherlock will help SaaS teams test AI chatbots, RAG systems, tool-using agents, and customer-data-connected AI apps before launch.

## Current Status

Sherlock has completed **Phase 13: Project Target Setup**.

The repository now contains the Phase 1 foundation, the static Phase 2 public website, the Phase 3 methodology documentation, the Phase 4 static sample report asset, the Phase 5 internal scanner engine foundation, the Phase 6 attack prompt library, the Phase 7 evaluator system, the Phase 8 manual audit workflow, the Phase 9 backend API foundation, the Phase 10 database foundation, the Phase 11 authentication and user accounts foundation, the Phase 12 dashboard/auth UI shell, and the Phase 13 project/target setup foundation:

- repository organization
- product and architecture documentation
- development notes
- security principles
- environment templates
- ignore/config hygiene
- public landing page
- sample report page with demo-only content
- public methodology page
- security/trust page
- pricing and early-access page
- contact, beta, and audit request UI
- detailed internal methodology
- vulnerability category taxonomy
- evidence standards
- severity, confidence, and finding status definitions
- report language standards
- polished public sample AI launch security report
- internal sample report reference document
- reusable static report content structure
- realistic demo findings with sanitized fictional evidence
- internal scanner engine package
- scan configuration loading and validation
- target adapter abstraction
- mock and generic HTTP/API target adapters
- safe internal smoke test runner
- local JSON scan output and summary files
- internal attack prompt/test-case library
- versioned prompt library manifest and schema
- category-based prompt/test files mapped to the methodology
- prompt library loader and validator utilities
- deterministic evaluator system package
- structured evaluation results, redacted evidence, and manual-review flags
- local evaluator CLI and unittest coverage
- manual audit workflow documentation
- client intake, authorization, scope, checklist, playbook, evidence, finding review, delivery, retest, and closure procedures
- lightweight markdown templates for manual audit preparation
- backend API application skeleton under `apps/api`
- FastAPI health and version/status endpoints
- placeholder route modules for projects, targets, scans, findings, reports, and verification
- shared API response envelope, config loading, logging, CORS placeholder, structured error handling, and API foundation tests
- PostgreSQL/Supabase-compatible database schema documentation under `db/`
- initial SQL migration for organizations, profiles, memberships, projects, targets, verifications, scans, events, findings, reports, manual audits, retests, usage records, and audit logs
- local database setup notes, migration workflow, RLS planning, and privacy/security boundaries
- Supabase Auth-compatible architecture and setup documentation
- safe auth configuration placeholders without real keys
- backend auth helper/dependency foundation
- public auth status route and protected current-user route foundation
- current-user/profile/membership response schemas
- user profile, organization membership, role model, backend JWT validation, and future RLS strategy documentation
- static login, signup, and forgot-password UI shells
- protected-dashboard layout shell under `apps/web/dashboard/`
- dashboard overview, projects, scans, findings, reports, and settings pages
- dashboard navigation, workspace/account placeholders, empty states, status badges, loading/error state patterns, and disabled future-action controls
- optional browser-side display of the safe `GET /api/v0/auth/status` endpoint when the local API is running
- public website links to the Dashboard V0 and Login UI shell
- Phase 13 project setup page for AI app metadata
- Phase 13 target setup page for safe target metadata
- static project detail and target detail placeholders
- target type selector for API endpoint, OpenAI-compatible endpoint, Vercel AI SDK endpoint, RAG application, tool-using agent, chatbot URL, and manual audit target
- setup readiness progress showing project details, target metadata, authorization/scope, Phase 14 verification later, and Phase 15 scanning later
- disabled verify-target and run-scan actions with future-phase labels
- placeholder project/target API contract metadata documenting safe fields and forbidden secret fields

No public self-serve scan execution, backend scan execution APIs, production auth/session flow, production JWT verification, active API database persistence, real project persistence from the UI, real production project persistence, real target persistence from the UI, real scan creation, billing, queue workers, PDF generation, admin panel, target verification implementation, production scanner exposure, generated web reports, or real report generation are implemented.

## Product Positioning

PowerDetect Sherlock is intended to help teams identify launch security risks in AI products, including:

- prompt injection
- system prompt leakage
- sensitive data leakage
- RAG data exfiltration
- indirect prompt injection
- tool/function abuse
- unsafe output handling
- cost abuse and unbounded consumption

Passing a future Sherlock scan must never be treated as a complete guarantee of security. The product should provide evidence, risk findings, and remediation guidance, not absolute claims.

## Repository Structure

```text
.
|-- apps/
|   |-- api/             # Phase 9 FastAPI backend foundation with Phase 11 auth and Phase 13 contract placeholders
|   `-- web/             # Static public website plus dashboard/auth and Phase 13 setup UI shell
|-- config/              # Shared product metadata and future configuration
|-- db/                  # Phase 10 PostgreSQL/Supabase-compatible database foundation
|-- docs/                # Product, architecture, security, roadmap, and setup docs
|-- packages/            # Internal scanner engine, prompt library, evaluator system, and future shared libraries
|-- templates/           # Phase 8 lightweight manual audit templates
|-- .env.example         # Safe local environment template
|-- .gitignore           # Repository hygiene and generated artifact exclusions
|-- LICENSE
`-- README.md
```

The repository remains intentionally minimal. Phase 13 extends the static dashboard with project and target setup screens only; full platform behavior remains future phases.

## Documentation

- [Project Overview](docs/overview.md)
- [Architecture Vision](docs/architecture.md)
- [Development Setup](docs/development.md)
- [Backend API Foundation](apps/api/README.md)
- [Database Foundation](db/README.md)
- [Authentication and User Accounts](docs/auth.md)
- [Sherlock Methodology](docs/methodology.md)
- [Scanner Engine](docs/scanner-engine.md)
- [Prompt Library](docs/prompt-library.md)
- [Evaluator System](docs/evaluator-system.md)
- [Manual Audit Workflow](docs/audits/README.md)
- [Sample Report Reference](docs/sample-report.md)
- [Security Notes](docs/security.md)
- [Roadmap](docs/roadmap.md)
- [Scope Boundaries](docs/scope.md)
- [Phase 2 Public Website Notes](docs/phase-2-public-website.md)

## Development

Preview the static public website with Python:

```bash
python3 -m http.server 4173 --directory apps/web
```

Then open `http://localhost:4173/`.

Dashboard/auth/setup shell pages are available at:

```text
http://localhost:4173/login.html
http://localhost:4173/signup.html
http://localhost:4173/forgot-password.html
http://localhost:4173/dashboard/
http://localhost:4173/dashboard/projects.html
http://localhost:4173/dashboard/project-setup.html
http://localhost:4173/dashboard/project-detail.html
http://localhost:4173/dashboard/target-setup.html
http://localhost:4173/dashboard/target-detail.html
```

Install and run the backend API foundation:

```bash
python3 -m pip install -r apps/api/requirements.txt
PYTHONPATH=apps/api python3 -m uvicorn app.main:app --reload --port 8000
```

Then check `http://localhost:8000/health`.

The Phase 10 SQL migration can be applied to a local PostgreSQL/Supabase-compatible database:

```bash
createdb sherlock_local
psql "postgresql://localhost/sherlock_local" -v ON_ERROR_STOP=1 -f db/migrations/20260507100000_phase_10_initial_database_foundation.sql
```

There is still no live Supabase connection requirement, billing provider, queue worker, admin panel, PDF tooling, public scan feature, backend scanner execution endpoint, target verification flow, report generator, production JWT verification, production login/signup/session flow, real project persistence, real target persistence, or active API persistence path configured.

Run the internal Phase 5 mock scanner dry-run with Python:

```bash
python3 -m packages.scanner_engine.cli --config packages/scanner_engine/example.scan.json
```

This writes local scan artifacts under `scan-results/`, which is ignored by Git.

Validate the internal Phase 6 prompt library with Python:

```bash
python3 -m packages.prompt_library.validate
```

Run the internal Phase 7 evaluator tests with Python:

```bash
python3 -m unittest packages.evaluator_system.tests.test_evaluator
```

Review the Phase 8 manual audit workflow:

```bash
find docs/audits templates -maxdepth 2 -type f | sort
```

Keep `.env.local`, generated reports, scan outputs, logs, and build artifacts out of Git.

## Product Metadata

Shared product metadata lives in [config/product.json](config/product.json).
