# Sherlock Database Foundation

Status: Phase 10 Database Setup completed

This directory contains the database foundation for Sherlock, the AI Launch Security Audit + Scanner product under the PowerDetect brand.

Phase 10 defines a PostgreSQL/Supabase-compatible schema, migration structure, schema documentation, local setup guidance, and security boundaries. It does not connect the Phase 9 API routes to production persistence.

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

RLS is enabled in the initial migration with no user access policies. That is intentional: no customer-facing reads or writes should work until Phase 11 auth and later authorization phases define scoped policies.

## Seeds

No seed data is included in Phase 10. Future seed files must use fake/demo-only records, example domains, no real emails, no real target secrets, and no customer data.
