# Queue and Worker System — Phase 15

## Overview

Phase 15 establishes the **queue and worker system foundation** for PowerDetect Sherlock. It prepares the platform to run future scans asynchronously through background workers instead of direct web request/response handlers.

This phase is **foundation only**. It does not implement public scan execution, production queue deployment, real network scanning, billing, or report generation.

---

## Architecture

```text
                        ┌─────────────────────┐
                        │   Backend API        │
                        │   (FastAPI)          │
                        │                     │
                        │  POST /api/v0/scans │  ← future authenticated endpoint
                        │  GET  /api/v0/scans │  ← queue contract placeholder
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │   Queue Backend      │
                        │                     │
                        │  LocalMemoryQueue   │  ← Phase 15 dev backend
                        │  (future: Redis/RQ) │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │   Worker Engine      │
                        │                     │
                        │  Safety gates       │
                        │  Job dispatch       │
                        │  Scanner execution  │  ← Phase 5 MockTargetAdapter only
                        │  Result storage     │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │  Phase 5 Scanner    │
                        │  Phase 6 Prompts    │  ← future integration
                        │  Phase 7 Evaluator  │  ← future integration
                        └─────────────────────┘
```

---

## Queue Abstraction

### Backend Interface

The `QueueBackend` abstract class defines a clean interface that can be swapped between implementations:

- `enqueue(payload)` — add a job to the queue
- `dequeue()` — remove and return the next job
- `get_status(job_id)` — check job status
- `update_status(job_id, status)` — update status
- `store_result(result)` — store a completed result
- `get_result(job_id)` — retrieve a result
- `pending_count()` — count pending jobs
- `list_jobs()` — list all known jobs

### Local In-Memory Backend

`LocalMemoryQueue` is a thread-safe in-memory implementation for development and testing. It does not persist across process restarts.

### Future Redis/RQ Backend

A future phase can add a Redis-backed implementation:

1. Install `rq` (Redis Queue) — simpler than Celery for a solo founder MVP
2. Implement `QueueBackend` with Redis-backed storage
3. Set `QUEUE_BACKEND=redis` and `REDIS_URL` in `.env.local`
4. Keep all job payloads JSON-serializable for safe serialization
5. Avoid insecure pickle serialization for untrusted jobs

Celery is also acceptable if the implementation remains minimal. The queue abstraction supports either approach.

---

## Job Types

| Type | Purpose | Phase 15 Status |
|---|---|---|
| `scan.run` | Execute a scan against a verified target | Mock only via Phase 5 MockTargetAdapter |
| `scan.evaluate` | Run Phase 7 evaluator on scan results | Placeholder — returns success with message |
| `scan.summarize` | Summarize scan findings | Placeholder |
| `report.prepare_placeholder` | Prepare report draft | Placeholder |

---

## Job Lifecycle States

| Status | Description | Terminal? |
|---|---|---|
| `queued` | Job is waiting in the queue | No |
| `running` | Worker has picked up the job | No |
| `completed` | Job finished successfully | Yes |
| `failed` | Job encountered an error | Yes |
| `cancelled` | Job was cancelled before completion | Yes |
| `timed_out` | Job exceeded its timeout | Yes |
| `blocked_unverified` | Blocked because target is not verified | Yes |
| `blocked_unsafe` | Blocked by a safety gate | Yes |

### Allowed Transitions

- `queued` → `running`, `cancelled`, `blocked_unverified`, `blocked_unsafe`
- `running` → `completed`, `failed`, `cancelled`, `timed_out`
- Terminal states have no outgoing transitions

---

## Job Payload Schema

All payloads must be JSON-serializable. **Do NOT include secrets.**

```json
{
  "job_id": "uuid",
  "job_type": "scan.run",
  "project_id": "",
  "target_id": "",
  "scan_id": "",
  "organization_id": "",
  "requested_by_user_id": "",
  "scan_type": "safe_smoke",
  "verification_status": "verified",
  "target_snapshot": {
    "name": "My Target",
    "type": "mock"
  },
  "limits": {
    "max_tests": 25,
    "timeout_seconds": 300
  },
  "created_at": "2026-05-08T00:00:00Z",
  "metadata": {}
}
```

### Forbidden Payload Fields

The following field names are rejected by safety gates:

`api_key`, `api_secret`, `bearer_token`, `access_token`, `refresh_token`, `password`, `passwd`, `private_key`, `secret_key`, `cookie`, `session_token`, `x_api_key`, `authorization_header`, `raw_header`, `credential`

---

## Worker Result Schema

```json
{
  "job_id": "uuid",
  "status": "completed",
  "started_at": "2026-05-08T00:00:01Z",
  "completed_at": "2026-05-08T00:00:02Z",
  "duration_ms": 42,
  "output_reference": "worker-output/shk_.../scan-result.json",
  "summary": {},
  "error_code": "",
  "error_message": "",
  "safety_decision": "mock_scan_only",
  "metadata": {
    "scan_id": "shk_...",
    "adapter": "mock",
    "network_used": false,
    "phase": "phase_15_worker_foundation"
  }
}
```

---

## Safety Gates

Before any job executes, the worker checks these gates in order:

1. **queue_enabled** — `WORKER_ENABLED` must be `true` (skipped for local dry-runs)
2. **target_verified** — `verification_status` must be `verified`
3. **job_type_allowed** — must be a recognized job type
4. **target_url_safe** — blocks private/internal/localhost/metadata-service URLs
5. **no_secrets_in_payload** — rejects fields that look like API keys, tokens, passwords
6. **limits** — `max_tests` and `timeout_seconds` must not exceed configured maximums
7. **scan_type_limits** (Phase 16) — checks scan type limits, category mapping, and verification rules

If any gate fails, the job is blocked with `blocked_unverified` or `blocked_unsafe` status and an error message explaining which gate failed.

### URL Safety Check

The basic URL check blocks:
- `localhost`, `127.0.0.1`, `0.0.0.0`, `[::1]`
- `169.254.x.x` (link-local / cloud metadata)
- `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x` (RFC 1918 private)
- `metadata.google`, `metadata.aws`

Full SSRF hardening (DNS rebinding, redirect following, IP resolution) is Phase 22.

---

## Local Worker CLI

Run a safe mock worker dry-run from the repository root:

```bash
python3 -m packages.worker_system.cli
```

This will:
1. Generate a demo mock job payload with `verification_status: verified`
2. Validate all safety gates
3. Execute a mock scan using Phase 5 `MockTargetAdapter` (no network requests)
4. Write the result to `worker-output/`

Options:

```bash
python3 -m packages.worker_system.cli --stdout          # print result to stdout
python3 -m packages.worker_system.cli --validate-only   # only check safety gates
python3 -m packages.worker_system.cli --job job.json    # load a custom job payload
python3 -m packages.worker_system.cli --output-dir dir  # custom output directory
```

Output files go to `worker-output/` which is ignored by Git.

---

## How Phase 5 Scanner, Phase 6 Prompts, and Phase 7 Evaluator Connect

### Current Phase 15

- `scan.run` jobs use the Phase 5 `ScannerEngine` with `MockTargetAdapter`
- The scanner runs `safe_smoke` tests (benign prompts from `packages/scanner_engine/prompts.py`)
- No real network requests are made
- The Phase 6 prompt library is not automatically loaded by the worker yet
- The Phase 7 evaluator is not automatically invoked by the worker yet

### Future Integration

1. **scan.run** will load Phase 6 prompt library test cases via `packages.prompt_library.select_test_cases()`, convert them to `ScannerTest` objects, and execute them through a real target adapter
2. **scan.evaluate** will invoke `packages.evaluator_system.evaluate_scan_result()` on the scan output
3. **scan.summarize** will aggregate evaluator output into a findings summary
4. **report.prepare_placeholder** will format findings into a report draft

---

## Environment Configuration

| Variable | Default | Purpose |
|---|---|---|
| `QUEUE_BACKEND` | `local` | Queue backend type (`local` for in-memory, `redis` future) |
| `REDIS_URL` | placeholder | Redis connection URL for future Redis/RQ backend |
| `WORKER_ENABLED` | `false` | Enable worker execution (must be `true` for production) |
| `WORKER_MAX_CONCURRENT_JOBS` | `1` | Maximum concurrent jobs per worker |
| `WORKER_JOB_TIMEOUT_SECONDS` | `300` | Maximum job execution time in seconds |
| `SCAN_MAX_TESTS_PER_JOB` | `25` | Maximum test cases per scan job |

---

## Why Public Scans Remain Disabled

Public scan creation is blocked until:

- Production authentication verifies user identity (Phase 11 foundation exists)
- Target ownership verification confirms authorization (Phase 14 foundation exists)
- SSRF protection prevents scanning private/internal networks (Phase 22)
- Rate limits prevent abuse (Phase 22)
- Spend controls prevent unbounded cost (Phase 22)
- Audit logging tracks all scan activity (Phase 22)
- Queue workers process jobs safely outside request handlers (Phase 15 foundation exists)

The Phase 15 worker foundation prepares the async execution path. It does not unlock public scanning.

---

## Future Production Deployment

Production queue deployment may include:

- Redis or managed queue service as the backend
- Separate worker process(es) running on dedicated infrastructure
- Health checks and monitoring for worker processes
- Dead letter queue for failed jobs
- Job retry policies with backoff
- Concurrency limits and queue depth monitoring
- Graceful shutdown and job draining
- Secret management for worker credentials

These are **not implemented** in Phase 15.

---

## Files

### Created
- `packages/worker_system/__init__.py` — package exports
- `packages/worker_system/jobs.py` — job payload, result, lifecycle, types
- `packages/worker_system/queue.py` — queue abstraction and local backend
- `packages/worker_system/safety.py` — safety gate checks
- `packages/worker_system/worker.py` — worker engine
- `packages/worker_system/cli.py` — local worker CLI
- `packages/worker_system/README.md` — package documentation
- `packages/worker_system/tests/__init__.py` — test package init
- `packages/worker_system/tests/test_worker_system.py` — unit tests
- `docs/workers.md` — this document

### Modified
- `apps/api/app/schemas/scans.py` — queue contract schemas
- `apps/api/app/routes/scans.py` — queue contract in placeholder response
- `apps/api/app/routes/version.py` — updated scans module status + queue_backend boundary
- `apps/api/app/config.py` — worker_enabled and queue_backend config fields
- `apps/api/app/main.py` — updated description
- `apps/api/tests/test_api_foundation.py` — added scans contract test
- `apps/web/dashboard/scans.html` — queue status messaging and lifecycle reference
- `apps/web/dashboard/index.html` — Phase 15 banner and activity
- `.env.example` — queue/worker config placeholders
- `.gitignore` — worker-output and worker-results directories
- `config/product.json` — updated phase
- `docs/workers.md` — new documentation
