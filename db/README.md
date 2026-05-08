# Sherlock Database Foundation

Status: Phase 10 Database Setup completed; Phase 11 auth alignment documented; Phase 13 setup UI does not use active persistence

This directory contains the database foundation for Sherlock, the AI Launch Security Audit + Scanner product under the PowerDetect brand.

Phase 10 defines a PostgreSQL/Supabase-compatible schema, migration structure, schema documentation, local setup guidance, and security boundaries. Phase 11 documents how this schema will align with Supabase Auth and adds backend auth placeholders. Phase 12 adds static dashboard/auth UI pages, and Phase 13 adds static project/target setup pages, but neither connects API routes or browser UI to production persistence.

## Selected Technology

Sherlock does not currently have a database framework, ORM, migration runner, or Supabase project configuration. Phase 10 therefore uses plain PostgreSQL SQL migrations under `db/migrations`.

This keeps the foundation:

- compatible with future Supabase/Postgres deployment
- understandable for a solo founder
- dependency-free for the existing FastAPI app
- easy to inspect and apply manually in local development
- separate from future auth, dashboard, worker, billing, and report-generation phases

## Structure

```text
db/
|-- README.md
|-- schema.md
|-- migrations/
|   `-- 20260507100000_phase_10_initial_database_foundation.sql
`-- seeds/
    `-- README.md
```

## What Phase 10 Adds

- Initial PostgreSQL schema for core Sherlock platform entities
- UUID primary keys using `gen_random_uuid()` from `pgcrypto`
- Timestamp fields and an `updated_at` trigger helper
- Foreign-key relationships between organizations, profiles, projects, targets, scans, findings, reports, audits, retests, usage records, and audit logs
- PostgreSQL enum types for controlled status/type/role values
- Check constraints for structural invariants such as non-empty names, valid URL shape, timestamps, and non-negative quantities
- JSONB metadata columns for safe extensibility
- Row Level Security enabled on application tables with no permissive policies yet
- Documentation for local setup, relationships, and security boundaries

## What Phase 10 Does Not Add

- Authentication flows
- Login/signup
- Sessions
- Authorization policies for real users
- Dashboard integration
- Project/target persistence from the UI
- Billing or Stripe integration
- Queue workers
- Public scan execution
- Scanner-to-database production integration
- Target ownership verification logic
- PDF/report generation
- Admin panel
- Real customer data storage
- Real email/contact form storage
- Production database credentials

## Phase 11 Auth Alignment

Supabase Auth is the intended auth provider. Supabase stores identity users in the managed `auth` schema.

Sherlock app-level account data should remain in the application tables:

- `public.user_profiles` for product profile metadata
- `public.organizations` for tenant/workspace records
- `public.organization_members` for membership and role records

Future auth-aware migrations should align `public.user_profiles.id` with `auth.users.id`. No Phase 11 migration is added because the existing Phase 10 schema already has the required foundation and RLS remains deny-by-default.

## Migration Workflow

Apply the initial migration to a local PostgreSQL database or Supabase local database only after creating a safe local database.

Example with local PostgreSQL:

```bash
createdb sherlock_local
psql "postgresql://localhost/sherlock_local" -f db/migrations/20260507100000_phase_10_initial_database_foundation.sql
```

Example with a Supabase local database connection string:

```bash
psql "$DATABASE_URL" -f db/migrations/20260507100000_phase_10_initial_database_foundation.sql
```

Do not commit real connection strings. Use `.env.local`, which is ignored by Git.

## Validation

If `psql` is available, validate the migration against an empty local database:

```bash
createdb sherlock_phase10_validation
psql "postgresql://localhost/sherlock_phase10_validation" -v ON_ERROR_STOP=1 -f db/migrations/20260507100000_phase_10_initial_database_foundation.sql
```

Drop the validation database after checking it if you no longer need it:

```bash
dropdb sherlock_phase10_validation
```

## Security Boundary

The schema is not production-ready by itself. Before any production use, future phases must add:

- Supabase Auth or another authentication provider
- authorization checks in backend routes and workers
- tenant-scoped RLS policies tied to authenticated users
- target ownership verification before public scanning
- encrypted or managed secret storage for target credentials
- retention/deletion workflows for scan and evidence data
- audit-log write paths and review procedures
- rate limits, spend limits, queue isolation, and SSRF controls

RLS is enabled in the initial migration with no user access policies. That is intentional: no customer-facing reads or writes should work until future reviewed auth-aware RLS policies define scoped access through `auth.uid()` and organization membership.

## Phase 13 Setup Notes

The existing `projects` and `targets` tables are sufficient as a foundation for Phase 13 static setup UI, so no database migration is added. The dashboard forms preview project and target metadata locally only.

Before enabling active persistence, reconcile the Phase 13 UI target labels with the Phase 10 `target_type` enum. The UI uses generic labels such as RAG application, tool-using agent, and manual audit target, while the Phase 10 enum currently includes `api_endpoint`, `openai_compatible`, `vercel_ai_sdk`, `langchain`, `llamaindex`, `chatbot_url`, and `manual`.

## Seeds

No seed data is included in Phase 10. Future seed files must use fake/demo-only records, example domains, no real emails, no real target secrets, and no customer data.
