# Scope Boundaries

Sherlock has completed Phase 8 Manual Audit Workflow.

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

## Out of Scope Through Phase 8

- API endpoints
- database migrations
- authentication
- dashboard UI
- admin panel
- billing
- queue workers
- report generation
- PDF export
- backend report APIs
- database persistence
- target verification logic
- public scan execution
- production deployment configuration
- real customer data handling
- LLM-as-judge behavior
- complex ML classifiers
- browser automation scanner
- CI/GitHub integration
- destructive testing automation
- unauthorized target scanning
- public self-serve scan feature

## Naming Rules

- Repository name: Sherlock
- Product name: Sherlock
- Brand/company identity: PowerDetect
- Full marketing name: PowerDetect Sherlock

Do not rename the repository or root folder.

## Phase Gate

Phase 8 establishes the manual audit workflow required before future report generation, backend, and worker phases. Future phases should use `docs/methodology.md` as the source of truth for category, evidence, severity, confidence, status, and reporting rules, `docs/sample-report.md` as a non-executable reference for report content structure, `docs/scanner-engine.md` as the scanner architecture reference, `docs/prompt-library.md` as the prompt library format reference, `docs/evaluator-system.md` as the evaluator contract reference, and `docs/audits/README.md` as the manual audit workflow reference.
