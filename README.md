# Sherlock

Sherlock is an AI Launch Security Audit + Scanner product under the PowerDetect brand.

The full marketing name is **PowerDetect Sherlock**. Sherlock will help SaaS teams test AI chatbots, RAG systems, tool-using agents, and customer-data-connected AI apps before launch.

## Current Status

Sherlock has completed **Phase 8: Manual Audit Workflow**.

The repository now contains the Phase 1 foundation, the static Phase 2 public website, the Phase 3 methodology documentation, the Phase 4 static sample report asset, the Phase 5 internal scanner engine foundation, the Phase 6 attack prompt library, the Phase 7 evaluator system, and the Phase 8 manual audit workflow:

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

No public self-serve scan execution, backend scan APIs, authenticated dashboard, auth, database migrations, billing, queue workers, PDF generation, admin panel, or real report generation are implemented.

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
|   `-- web/             # Phase 2 static public website
|-- config/              # Shared product metadata and future configuration
|-- docs/                # Product, architecture, security, roadmap, and setup docs
|-- packages/            # Internal scanner engine, prompt library, evaluator system, and future shared libraries
|-- templates/           # Phase 8 lightweight manual audit templates
|-- .env.example         # Safe local environment template
|-- .gitignore           # Repository hygiene and generated artifact exclusions
|-- LICENSE
`-- README.md
```

The repository is intentionally minimal until the frontend/backend stack is selected in later phases.

## Documentation

- [Project Overview](docs/overview.md)
- [Architecture Vision](docs/architecture.md)
- [Development Setup](docs/development.md)
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

There is still no package manager, backend runtime, database, auth provider, billing provider, queue worker, dashboard, admin panel, PDF tooling, public scan feature, or report generator configured.

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
