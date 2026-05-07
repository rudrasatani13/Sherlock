# Apps

This directory is reserved for future deployable Sherlock applications.

Current apps:

- `web`: static public website for PowerDetect Sherlock, introduced in Phase 2, refreshed in Phase 3, and expanded with the Phase 4 sample report

Expected future apps:

- `web`: may later expand beyond static pages into dashboard and authenticated product UI
- `api`: backend HTTP API for scan creation, report access, billing callbacks, and integrations

No backend API, public scanner execution, report generation, PDF export, authenticated dashboard, admin panel, billing flow, database, or queue code is implemented through Phase 8. The internal scanner engine lives under `../packages/scanner_engine`, the internal prompt library lives under `../packages/prompt_library`, the internal evaluator system lives under `../packages/evaluator_system`, and the manual audit workflow lives under `../docs/audits`; none of them are apps. A package manager or frontend framework should only be introduced when a later phase needs it.
