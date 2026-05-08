# Sherlock Worker System

Status: Phase 15 Queue + Worker System foundation completed

This package provides the queue and worker foundation for PowerDetect Sherlock. It prepares the system to run future scans asynchronously through background workers instead of direct web request/response handlers.

## Phase 15 Scope

Phase 15 is worker/queue foundation only:

- queue abstraction with a local in-memory development backend
- job payload and result schemas (JSON-serializable)
- scan job lifecycle states
- safety gate checks (verification, URL safety, secret rejection, limits)
- local worker engine with mock scan execution via Phase 5 scanner
- local worker CLI for dry-runs
- no external target scanning
- no production queue deployment
- no real Redis, Supabase, or secrets required

## Package Structure

```text
packages/worker_system/
|-- __init__.py
|-- cli.py          # Local worker CLI
|-- jobs.py         # Job payload, result, lifecycle, and type definitions
|-- queue.py        # Queue abstraction and local in-memory backend
|-- safety.py       # Safety gate checks
|-- worker.py       # Worker engine
|-- README.md
```

## Job Types

| Type | Purpose | Phase 15 |
|---|---|---|
| `scan.run` | Execute a scan against a verified target | Mock only |
| `scan.evaluate` | Run evaluator on scan results | Placeholder |
| `scan.summarize` | Summarize scan findings | Placeholder |
| `report.prepare_placeholder` | Prepare report draft | Placeholder |

## Job Lifecycle States

| Status | Description |
|---|---|
| `queued` | Job is waiting in the queue |
| `running` | Worker has picked up the job |
| `completed` | Job finished successfully |
| `failed` | Job encountered an error |
| `cancelled` | Job was cancelled before completion |
| `timed_out` | Job exceeded its timeout |
| `blocked_unverified` | Blocked because target is not verified |
| `blocked_unsafe` | Blocked by a safety gate |

## Safety Gates

Before any job executes, the worker checks:

1. **Queue enabled** — `WORKER_ENABLED` must be true (skipped for local dry-runs)
2. **Target verified** — `verification_status` must be `verified`
3. **Job type allowed** — must be a recognized job type
4. **Target URL safe** — no private/internal/localhost addresses
5. **No secrets in payload** — rejects fields that look like API keys, tokens, passwords
6. **Limits** — `max_tests` and `timeout_seconds` must not exceed configured maximums

## Local CLI

Run a safe mock worker dry-run from the repository root:

```bash
python3 -m packages.worker_system.cli
```

Options:

```bash
python3 -m packages.worker_system.cli --stdout
python3 -m packages.worker_system.cli --validate-only
python3 -m packages.worker_system.cli --job path/to/job.json
python3 -m packages.worker_system.cli --output-dir worker-output
```

Output is written to `worker-output/` which is ignored by Git.

## Queue Abstraction

The `QueueBackend` abstract class defines the interface:

- `enqueue(payload)` — add a job
- `dequeue()` — get the next job
- `get_status(job_id)` — check job status
- `update_status(job_id, status)` — update status
- `store_result(result)` — store a result
- `get_result(job_id)` — retrieve a result
- `pending_count()` — count pending jobs
- `list_jobs()` — list all known jobs

`LocalMemoryQueue` is the Phase 15 in-memory implementation. It is thread-safe but does not persist across restarts.

## Future Queue Backend

A future phase can swap the local backend for Redis/RQ or Celery:

- Implement `QueueBackend` with a Redis-backed store
- Configure `REDIS_URL` and `QUEUE_BACKEND=redis` in `.env.local`
- Add `rq` or `celery` to requirements
- Keep job payloads JSON-serializable for safe serialization

## Security Boundaries

- No secrets in job payloads
- No external target scanning in Phase 15
- Mock adapter only — no network requests
- SSRF hardening is Phase 22
- Production queue deployment is future work
- Public scan creation remains disabled
