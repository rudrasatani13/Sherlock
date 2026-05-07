# Architecture Vision

Sherlock is planned as a modular AI launch security audit and scanner platform. The architecture should keep customer-facing workflows, scan execution, prompt libraries, evaluators, reports, and billing separated so each area can evolve without becoming tightly coupled.

This document describes the future direction and the current Phase 8 manual audit workflow foundation. Phase 8 does not implement backend APIs, authentication, database storage, billing, queue workers, report generation, PDF export, admin panels, or public scan execution.

## Planned Components

### Web App, Dashboard, and Public Website

The future web app will cover the public website, authenticated dashboard, scan setup flows, report viewing, team/account settings, and billing surfaces.

Phase 2 implements the public website as a static site under `apps/web`. Authenticated dashboard work, scan setup flows, report viewing, team/account settings, and billing surfaces remain future phases.

Phase 4 expands the static public sample report page. It is a demo-only artifact, not a real report viewer and not generated from a scan.

### Methodology and Finding Taxonomy

The Phase 3 methodology is documented in `docs/methodology.md`. It defines the vulnerability categories, evidence standards, severity model, confidence model, finding statuses, report language standards, and future implementation guidance.

The methodology should remain separate from executable scanner logic, prompt text, evaluator code, and report rendering. Future implementation phases should reference the methodology rather than duplicating taxonomy rules in scattered code or page copy.

### Backend API

The backend API will eventually handle scan configuration, account data, report access, billing webhooks, target verification, and integration endpoints. API boundaries should be designed around explicit contracts and should avoid leaking scanner internals into UI code.

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

### Manual Audit Workflow

The manual audit workflow turns intake, authorization, scanner observations, prompt-library scenarios, evaluator outputs, manual validation, evidence handling, finding review, delivery, retesting, and closure into a repeatable human-led process.

Phase 8 adds documentation under `docs/audits` and lightweight templates under `templates`. It is a process layer only and does not add backend APIs, persistence, dashboard screens, report generation, PDF export, admin review panels, queue workers, billing, auth, public scan execution, or destructive testing automation.

### Async Scan Workers

Long-running scans should eventually run outside request/response paths through workers and queues. The worker layer should enforce timeouts, concurrency limits, retry policy, spend limits, and cancellation.

### Database and Auth

The database will eventually store accounts, users, scan configurations, ownership verification state, scan runs, findings, report metadata, billing state, and audit logs.

Authentication and authorization should be added before any customer data or scan target data is stored.

### Report System

Reports will eventually present evidence, severity, reproduction context, limitations, and remediation guidance. Reports must redact sensitive data and must avoid claiming that a target is fully secure.

Future reports should follow the severity, confidence, finding status, evidence, and language standards in `docs/methodology.md`.

The Phase 4 sample report reference in `docs/sample-report.md` documents a static content structure and fictional demo findings. It is not executable schema, report generation logic, a persistence model, or a PDF export system.

The Phase 8 report delivery workflow in `docs/audits/REPORT_DELIVERY.md` describes how an auditor can manually prepare and deliver a scoped report before report generation exists.

Generated reports should not be committed to the repository.

### Billing

Billing should be added after the core audit workflow and report value are proven. Billing events must be handled server-side and verified before granting usage.

### Local Runner

A local runner may eventually support customer-controlled testing against private environments. It should minimize data transfer, clearly explain what leaves the customer's environment, and avoid unsafe default network reachability.

### GitHub and CI Integration

Future GitHub/CI integration may allow teams to run approved checks before launch. It should use explicit target verification, scoped credentials, safe logging, and clear failure behavior.

## Repository Direction

The current foundation uses:

- `apps/` for future deployable applications
- `packages/` for future shared libraries and core domain modules
- `config/` for shared product metadata and future configuration
- `docs/` for product, architecture, setup, roadmap, security, and scope notes

The project should stay minimal until a real implementation phase needs a framework, package manager, database, queue, or deployment target.
