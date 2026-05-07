# Sherlock Database Schema

Status: Phase 10 Database Setup completed

This document describes the Phase 10 PostgreSQL/Supabase-compatible database foundation for Sherlock.

The schema is a foundation for future platform phases. It is not connected to production API persistence yet.

## Purpose

The database will eventually store the core records needed by PowerDetect Sherlock:

- organizations/workspaces
- future app-level user profiles
- memberships and roles
- projects and AI app metadata
- target metadata and verification records
- scan job metadata and lifecycle events
- reviewed findings
- report metadata
- manual audit engagement records
- retest records
- usage/billing placeholders
- security audit logs

## Entity Relationship Overview

```text
organizations
|-- organization_members
|   `-- user_profiles
|-- projects
|   |-- targets
|   |   `-- target_verifications
|   |-- scans
|   |   |-- scan_events
|   |   |-- findings
|   |   `-- reports
|   |-- findings
|   |   `-- retests
|   |-- reports
|   `-- manual_audits
|-- usage_records
`-- audit_logs
    `-- user_profiles
```

Core relationship rules:

- An organization is the top-level tenant/workspace container.
- A user profile may belong to many organizations through organization memberships.
- A project belongs to one organization.
- A target belongs to one project.
- A target verification record belongs to one target.
- A scan belongs to one project and may optionally reference one target.
- Scan events belong to one scan.
- A finding belongs to one project and may optionally reference one scan.
- A report belongs to one project and may optionally reference one scan.
- A manual audit belongs to one organization and may optionally reference one project.
- A retest may reference a finding, a scan, or both.
- Usage records and audit logs are organization-scoped foundations for future billing and security review.

## Tables

### organizations

Workspace/team/company container.

Key fields:

- `id`
- `name`
- `slug`
- `plan`
- `status`
- `metadata`
- `created_at`
- `updated_at`

Allowed statuses: `active`, `trial`, `suspended`, `archived`.

### user_profiles

Future app-level user metadata connected to an auth provider later.

Key fields:

- `id`
- `email`
- `display_name`
- `metadata`
- `created_at`
- `updated_at`

Phase 10 does not implement authentication. If Supabase Auth is used in Phase 11, `user_profiles.id` should map to `auth.users.id` through future auth-aware migrations and policies.

### organization_members

Future organization membership and role records.

Key fields:

- `id`
- `organization_id`
- `user_id`
- `role`
- `created_at`

Allowed roles: `owner`, `admin`, `member`, `viewer`.

### projects

AI app/product being tested.

Key fields:

- `id`
- `organization_id`
- `name`
- `description`
- `app_type`
- `environment`
- `status`
- `metadata`
- `created_at`
- `updated_at`

Allowed environments: `development`, `staging`, `production`, `demo`, `other`.

Allowed statuses: `draft`, `active`, `archived`.

### targets

Endpoint/chatbot/API/RAG/agent target configuration metadata.

Key fields:

- `id`
- `project_id`
- `target_type`
- `name`
- `url`
- `method`
- `auth_type`
- `safe_metadata`
- `is_verified`
- `created_at`
- `updated_at`

Allowed target types:

- `api_endpoint`
- `openai_compatible`
- `vercel_ai_sdk`
- `langchain`
- `llamaindex`
- `chatbot_url`
- `manual`

Target rows must not contain real API keys, bearer tokens, cookies, passwords, private keys, or raw headers. Future credentials must use secret management or encrypted storage.

### target_verifications

Future ownership verification records.

Key fields:

- `id`
- `target_id`
- `verification_type`
- `status`
- `challenge_hash`
- `challenge_reference`
- `verified_at`
- `expires_at`
- `created_at`

Allowed statuses: `pending`, `verified`, `failed`, `expired`.

Phase 10 does not implement verification logic or unlock scanning.

### scans

Scan job/request metadata.

Key fields:

- `id`
- `project_id`
- `target_id`
- `scan_type`
- `status`
- `started_at`
- `completed_at`
- `summary`
- `created_at`
- `updated_at`

Allowed scan types: `quick`, `standard`, `deep`, `manual`.

Allowed statuses: `pending`, `running`, `completed`, `failed`, `cancelled`.

Phase 10 does not implement scanner execution, queue workers, public scan creation, or persistence from public API routes.

### scan_events

Timeline/log of scan lifecycle events.

Key fields:

- `id`
- `scan_id`
- `event_type`
- `message`
- `metadata`
- `created_at`

Events may include future lifecycle changes, worker messages, cancellation notes, evaluator handoff summaries, or safe diagnostic metadata.

### findings

Reviewed vulnerability/risk findings from evaluator and/or manual review.

Key fields:

- `id`
- `scan_id`
- `project_id`
- `category`
- `title`
- `severity`
- `confidence`
- `status`
- `description`
- `business_impact`
- `evidence_summary`
- `recommendation`
- `metadata`
- `created_at`
- `updated_at`

Allowed severity values: `critical`, `high`, `medium`, `low`, `informational`.

Allowed confidence values: `high`, `medium`, `low`.

Allowed finding statuses: `open`, `fixed`, `accepted_risk`, `false_positive`, `needs_manual_review`, `inconclusive`.

Raw evidence should not be stored by default. `evidence_summary` should contain report-safe, redacted summaries only.

### reports

Future generated report metadata.

Key fields:

- `id`
- `scan_id`
- `project_id`
- `report_type`
- `status`
- `storage_path`
- `metadata`
- `created_at`
- `updated_at`

Allowed statuses: `draft`, `ready`, `delivered`, `archived`, `failed`.

Phase 10 does not implement report generation, PDF export, report storage, or report access routes.

### manual_audits

Future record of Phase 8 human-led audit engagements.

Key fields:

- `id`
- `organization_id`
- `project_id`
- `status`
- `scope_summary`
- `authorization_status`
- `started_at`
- `completed_at`
- `metadata`
- `created_at`
- `updated_at`

Allowed audit statuses: `draft`, `scoped`, `authorized`, `in_progress`, `delivered`, `closed`, `cancelled`.

Allowed authorization statuses: `pending`, `authorized`, `expired`, `revoked`, `not_required`.

### retests

Tracks retesting of specific findings or scans.

Key fields:

- `id`
- `finding_id`
- `scan_id`
- `status`
- `notes`
- `retested_at`
- `created_at`

Allowed statuses: `fixed`, `still_vulnerable`, `partially_fixed`, `inconclusive`, `accepted_risk`, `needs_manual_review`.

### usage_records

Future usage/billing foundation.

Key fields:

- `id`
- `organization_id`
- `usage_type`
- `quantity`
- `period_start`
- `period_end`
- `metadata`
- `created_at`

Phase 10 does not implement billing, Stripe, plan enforcement, or usage metering from app flows.

### audit_logs

Future security/audit logging.

Key fields:

- `id`
- `organization_id`
- `actor_user_id`
- `action`
- `entity_type`
- `entity_id`
- `metadata`
- `created_at`

Future phases should write audit logs for sensitive actions such as membership changes, target verification changes, scan creation, report access, billing events, and admin actions.

## Security and Privacy Model

Phase 10 security rules:

- Do not store real secrets in migrations or seeds.
- Do not store plain-text API keys, tokens, cookies, passwords, private keys, or raw auth headers in `targets`.
- Future target credentials must use managed secret storage or encrypted storage.
- Scan outputs may contain sensitive prompts, responses, retrieval traces, tool traces, or customer data.
- Raw evidence should not be stored by default.
- Report-safe evidence must be redacted before storage or delivery.
- Data retention and deletion workflows remain future work.
- Authentication, authorization, and RLS policies must be added before production use.
- The database must not be exposed publicly without auth and tenant-scoped RLS policies.

## RLS and Access-Control Plan

The Phase 10 migration enables RLS on application tables but adds no permissive user policies.

This is intentional because Phase 10 has no authentication provider, no sessions, and no dashboard.

Future Phase 11+ work should:

1. Connect `user_profiles.id` to the chosen auth provider.
2. Define organization membership lookup helpers.
3. Add organization-scoped read/write policies.
4. Use service-role access only in trusted server-side contexts.
5. Keep scanner workers scoped by explicit backend authorization and target verification.
6. Add audit logs for sensitive reads/writes where appropriate.

If Supabase Auth is selected, future policies can use `auth.uid()` to match `organization_members.user_id`, but Phase 10 does not create those policies.

## Local Setup Notes

Use a local PostgreSQL database or Supabase local database.

```bash
createdb sherlock_local
psql "postgresql://localhost/sherlock_local" -v ON_ERROR_STOP=1 -f db/migrations/20260507100000_phase_10_initial_database_foundation.sql
```

Keep real database URLs in `.env.local`, not in Git.

## Future Phase Readiness

Phase 10 prepares Phase 11 and later phases by creating stable table names, relationships, and constraints. Future work can add auth-aware policies, API persistence, dashboard reads/writes, target verification flows, workers, findings workflows, report access, billing, usage metering, and audit-log write paths in explicit scoped phases.
