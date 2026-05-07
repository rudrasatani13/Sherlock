# Authentication and User Accounts

Status: Phase 11 Authentication and User Accounts foundation completed

This document defines Sherlock's authentication and account foundation for future authenticated product usage. Sherlock will use Supabase Auth as the intended authentication provider, while keeping the current repository safe to run without a live Supabase project or real secrets.

Phase 11 is a foundation only. It does not add a dashboard, billing, queue workers, target verification, public scan execution, report generation, PDF export, an admin panel, or production RLS policies.

## Provider Direction

Sherlock intends to use Supabase Auth for user identity.

Supabase Auth stores authentication users in the Supabase-managed `auth` schema. Sherlock app-level account metadata should live in application tables such as `public.user_profiles`, `public.organizations`, and `public.organization_members`.

The future dashboard should prefer Supabase client-side auth for login/signup/session handling. The backend should validate Supabase-issued JWT bearer tokens before serving protected API routes.

## Current Phase 11 Behavior

A live Supabase connection is optional and not required for basic local checks.

The FastAPI backend now includes:

- `GET /api/v0/auth/status` as a public configuration/status endpoint
- `GET /api/v0/me` as a protected current-user route foundation
- auth configuration placeholders for Supabase URL, anon key, service-role key, JWKS URL, and an auth enable flag
- strict bearer-token parsing helper
- auth error responses using the shared API envelope

Token validation is not production-active in Phase 11. When auth is disabled or Supabase/JWKS configuration is incomplete, protected routes return `auth_unavailable` instead of trusting fake user IDs.

## Environment Configuration

Safe placeholders live in `.env.example`.

Relevant variables:

| Variable | Purpose |
| --- | --- |
| `AUTH_ENABLED` | Local feature flag for backend auth enforcement. Default placeholder is `false`. |
| `SUPABASE_URL` | Future Supabase project URL. Placeholder only in Git. |
| `SUPABASE_ANON_KEY` | Future browser-safe Supabase anon key. Placeholder only in Git. |
| `SUPABASE_SERVICE_ROLE_KEY` | Future server-only Supabase service-role key. Never expose to browser code. |
| `SUPABASE_JWKS_URL` | Future JWKS URL used by the backend to validate Supabase JWTs. Placeholder only in Git. |

Do not create or commit `.env.local` with real values. Do not commit real Supabase keys.

## User Profile Strategy

The Phase 10 table `public.user_profiles` is the app-level profile foundation.

Future mapping:

- `user_profiles.id` should match `auth.users.id`
- `email` may mirror the auth email for app display/search where appropriate
- `display_name` stores the user's preferred product display name
- `metadata` may hold optional profile fields such as avatar URL or onboarding status until a future reviewed migration adds dedicated columns
- `created_at` and `updated_at` track app-profile lifecycle

Profile creation should be added in a later reviewed phase using either a safe Supabase database trigger on `auth.users` or a trusted backend onboarding path. Phase 11 does not write profile records.

## Organization and Membership Strategy

Sherlock uses organizations as workspace/team/company tenants.

Relevant tables:

- `public.organizations`
- `public.organization_members`
- `public.user_profiles`

Future onboarding should create an organization and insert an `owner` membership for the authenticated user after signup or workspace creation. Organization membership is the source of truth for tenant access.

## Role Model

Organization member roles:

| Role | Future permissions |
| --- | --- |
| `owner` | Manage organization settings, members, projects, reports, and future billing. |
| `admin` | Manage projects, members, targets, scans, and reports, excluding owner-only actions. |
| `member` | Create or run future authorized scans depending on plan and target verification state. |
| `viewer` | Read future project and report surfaces without creating scans or changing settings. |

Phase 11 documents the model only. It does not enforce project/report permissions yet because active persistence and dashboard flows are still future work.

## Backend Token Validation Strategy

Future production backend behavior should:

1. Require `Authorization: Bearer <supabase-access-token>` on protected routes.
2. Validate token signature using Supabase JWKS.
3. Validate issuer, audience, expiry, and subject claims.
4. Treat the token subject as the authenticated Supabase user ID.
5. Load app-level profile and organization memberships from protected database queries.
6. Enforce route-level authorization before reading or writing tenant data.

The backend must never trust user IDs supplied in request bodies for authentication or tenant access.

## RLS Strategy

RLS is enabled on Phase 10 application tables with no permissive policies. That deny-by-default posture remains safe for Phase 11.

Future RLS policies should use `auth.uid()` and `public.organization_members` to enforce organization boundaries. A user should only access organizations where they have a membership row.

Future policy direction:

- users can read their own profile
- users can read organizations where they are members
- owners/admins can manage members and project settings
- members may create/run scans only after target verification, plan checks, and abuse controls exist
- viewers can read future report/project surfaces only
- service-role access is backend-only and must bypass RLS only inside trusted server-side code paths

Do not add broad public policies. Do not expose tables before policies are reviewed.

## Security Boundaries

- The service-role key must never be exposed to browser/frontend code.
- Real secrets must stay in ignored local or managed deployment environments.
- Login/signup UI is not implemented in Phase 11.
- The static public website remains a public marketing site, not a dashboard.
- Auth routes do not expose scanner, prompt-library, evaluator, target-verification, report-generation, billing, admin, or worker behavior.
- Production JWT validation and production RLS policies remain future reviewed work.
