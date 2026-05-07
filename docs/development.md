# Development Setup

Sherlock has completed Phase 8 Manual Audit Workflow. There is a static public website under `apps/web`, an internal Python scanner foundation under `packages/scanner_engine`, an internal prompt library under `packages/prompt_library`, an internal evaluator system under `packages/evaluator_system`, and manual audit workflow documentation under `docs/audits` with templates under `templates`, but there is still no backend API, report generator, PDF export, database, queue, billing, auth, dashboard, admin panel, public scan feature, or package manager configured.

## Current Requirements

- Git
- A local editor
- Python 3 for simple local static preview, internal scanner dry-runs, prompt-library validation, local evaluator tests, and lightweight documentation checks

No Node.js package manager, database, Redis, auth provider, billing provider, report generator, PDF tooling, dashboard, admin panel, public scan feature, or external AI provider is required for Phase 8.

## Local Environment

Create a local environment file from the safe template:

```bash
cp .env.example .env.local
```

Only use placeholder values until a future phase actually needs an integration.

Do not commit `.env.local` or any other real environment file.

## Useful Checks

```bash
python3 -m http.server 4173 --directory apps/web
curl -I http://localhost:4173/
python3 -m packages.scanner_engine.cli --config packages/scanner_engine/example.scan.json
python3 -m packages.prompt_library.validate
python3 -m packages.evaluator_system.cli --input scan-results/<scan_id>/scan-result.json --stdout
python3 -m unittest packages.evaluator_system.tests.test_evaluator
find docs/audits templates -maxdepth 2 -type f | sort
git status --short
find . -maxdepth 3 -type f | sort
```

When a package manager is introduced later, this document should be updated with the exact install, lint, typecheck, test, and build commands.

## Future Setup Areas

Future phases may add:

- web app runtime
- backend API runtime
- shared TypeScript package setup
- database and migrations
- queue/worker runtime
- report generation tooling
- test framework
- CI checks

Do not add these until the corresponding phase needs them.
