# Apps

This directory is reserved for future deployable Sherlock applications.

Current apps:

- `web`: static public website for PowerDetect Sherlock, introduced in Phase 2, refreshed in Phase 3, expanded with the Phase 4 sample report, and extended in Phase 12 with static dashboard/auth UI shell pages
- `api`: minimal FastAPI backend API foundation introduced in Phase 9 and extended with Phase 11 auth foundation routes

Expected future apps:

- `web`: may later expand beyond static pages into a production authenticated product UI with real API consumption
- `api`: may later expand into authenticated platform APIs for projects, targets, scans, findings, reports, verification, billing callbacks, and integrations

Phase 10 adds the database foundation under `../db`, Phase 11 adds Supabase Auth-compatible backend auth placeholders, and Phase 12 adds static dashboard/auth UI pages under `web`. App routes still do not use active persistence. No public scanner execution, scanner execution API, report generation, PDF export, production authenticated dashboard API integration, admin panel, billing flow, target verification implementation, production login/signup/session flow, or queue code is implemented. The internal scanner engine lives under `../packages/scanner_engine`, the internal prompt library lives under `../packages/prompt_library`, the internal evaluator system lives under `../packages/evaluator_system`, and the manual audit workflow lives under `../docs/audits`.
