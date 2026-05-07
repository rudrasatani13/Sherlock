# Packages

This directory contains internal Sherlock packages.

Current packages:

- `scanner_engine`: Phase 5 Internal Scanner Engine V0 for controlled local testing only
- `prompt_library`: Phase 6 Attack Prompt Library V0 for internal reviewed test-case definitions
- `evaluator_system`: Phase 7 Evaluator System V0 for deterministic local evaluation of scanner results

Expected future package areas:

- shared product types and configuration
- report schema and report utilities
- integration helpers

The scanner engine, prompt library, and evaluator system are internal only. They do not implement backend scan APIs, auth, database persistence, queue workers, billing, dashboard integration, PDF generation, report generation, or public scanning.

Phase 9 adds a separate FastAPI backend foundation under `../apps/api`. It does not change package boundaries or expose these internal packages through public HTTP routes.
