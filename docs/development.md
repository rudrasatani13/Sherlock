# Development Setup

Sherlock has completed Phase 13 Project Target Setup. There is a static public website and static dashboard/auth/project-target setup UI shell under `apps/web`, a minimal FastAPI backend foundation under `apps/api`, a PostgreSQL/Supabase-compatible database foundation under `db/`, a Supabase Auth-compatible auth foundation documented in `docs/auth.md`, an internal Python scanner foundation under `packages/scanner_engine`, an internal prompt library under `packages/prompt_library`, an internal evaluator system under `packages/evaluator_system`, and manual audit workflow documentation under `docs/audits` with templates under `templates`.

There is still no active API database persistence, real production project persistence, target persistence from the UI, production JWT verification, production login/signup/session flow, live Supabase browser integration, report generator, PDF export, queue, billing, admin panel, public scan feature, target verification flow, or public scanner execution API configured.

## Current Requirements

- Git
- A local editor
- Python 3 for simple local static preview, the API foundation, internal scanner dry-runs, prompt-library validation, local evaluator tests, and lightweight documentation checks
- Optional local PostgreSQL or Supabase CLI setup if you want to apply the Phase 10 SQL migration locally
- Optional future Supabase project credentials for auth experiments, kept only in ignored local environment files

No Node.js package manager, Redis, live Supabase project, real auth keys, billing provider, report generator, PDF tooling, admin panel, public scan feature, target verification provider, queue worker, or external AI provider is required for Phase 13.

## Local Environment

Create a local environment file from the safe template:

```bash
cp .env.example .env.local
```

Only use placeholder values until a future phase actually needs an integration.

Do not commit `.env.local` or any other real environment file.

Phase 11 keeps `AUTH_ENABLED=false` by default, and Phases 12 and 13 do not change that. With placeholders or missing Supabase values, `GET /api/v0/auth/status` is safe to call locally and protected routes such as `GET /api/v0/me` return auth unavailable rather than fake user data. The static login/settings pages can display this status if the local API is running.

## Useful Checks

```bash
python3 -m http.server 4173 --directory apps/web
curl -I http://localhost:4173/
curl -I http://localhost:4173/login.html
curl -I http://localhost:4173/dashboard/
curl -I http://localhost:4173/dashboard/project-setup.html
curl -I http://localhost:4173/dashboard/target-setup.html
python3 -m pip install -r apps/api/requirements.txt
PYTHONPATH=apps/api python3 -m uvicorn app.main:app --reload --port 8000
curl http://localhost:8000/health
curl http://localhost:8000/api/v0/auth/status
PYTHONPATH=apps/api python3 -m unittest discover -s apps/api/tests
createdb sherlock_local
psql "postgresql://localhost/sherlock_local" -v ON_ERROR_STOP=1 -f db/migrations/20260507100000_phase_10_initial_database_foundation.sql
python3 -m packages.scanner_engine.cli --config packages/scanner_engine/example.scan.json
python3 -m packages.prompt_library.validate
python3 -m packages.evaluator_system.cli --input scan-results/<scan_id>/scan-result.json --stdout
python3 -m unittest packages.evaluator_system.tests.test_evaluator
find docs/audits templates -maxdepth 2 -type f | sort
git status --short
find . -maxdepth 3 -type f | sort
```

The API dependency file is scoped to `apps/api/requirements.txt`. When broader package management, linting, typechecking, test orchestration, or build tooling is introduced later, this document should be updated with the exact commands.

## Future Setup Areas

Future phases may add:

- web app runtime
- production backend API runtime
- shared TypeScript package setup
- production Supabase Auth JWT validation and auth-aware RLS policies
- queue/worker runtime
- report generation tooling
- test framework
- CI checks

Do not add these until the corresponding phase needs them.
