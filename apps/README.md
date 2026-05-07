# Apps

This directory is reserved for future deployable Sherlock applications.

Current apps:

- `web`: static public website for PowerDetect Sherlock, introduced in Phase 2, refreshed in Phase 3, and expanded with the Phase 4 sample report
- `api`: minimal FastAPI backend API foundation introduced in Phase 9

Expected future apps:

- `web`: may later expand beyond static pages into dashboard and authenticated product UI
- `api`: may later expand into authenticated platform APIs for projects, targets, scans, findings, reports, verification, billing callbacks, and integrations

Phase 10 adds the database foundation under `../db`, but app routes still do not use active persistence. No public scanner execution, scanner execution API, report generation, PDF export, authenticated dashboard, admin panel, billing flow, target verification implementation, or queue code is implemented. The internal scanner engine lives under `../packages/scanner_engine`, the internal prompt library lives under `../packages/prompt_library`, the internal evaluator system lives under `../packages/evaluator_system`, and the manual audit workflow lives under `../docs/audits`.
