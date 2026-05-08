# Packages

This directory contains internal Sherlock packages.

Current packages:

- `scanner_engine`: Phase 5 Internal Scanner Engine V0 for controlled local testing only
- `prompt_library`: Phase 6 Attack Prompt Library V0 for internal reviewed test-case definitions
- `evaluator_system`: Phase 7 Evaluator System V0 for deterministic local evaluation of scanner results
- `worker_system`: Phase 15 Queue and Worker System foundation for local/mock job execution
- `scan_limits`: Phase 16 Scan Types + Limits foundation for bounded scan modes and validation
- `findings_system`: Phase 17 Findings System foundation for structured finding candidates, finalized finding objects, grouping, merging, sorting, redacted evidence summaries, and recommendation templates

Expected future package areas:

- shared product types and configuration
- report schema and report utilities
- integration helpers

The scanner engine, prompt library, evaluator system, worker system, scan limits, and findings system are internal only. They do not implement backend scan execution APIs, production auth, active database persistence, billing, production dashboard integration, PDF generation, report generation, active findings persistence, real customer evidence storage, or public scanning.

Phase 9 adds a separate FastAPI backend foundation under `../apps/api`. Phase 17 exposes only static findings schema metadata. It does not expose scanner execution, evaluator execution, findings persistence, report generation, or customer evidence through public HTTP routes.
