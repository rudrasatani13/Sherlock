# Authentication and User Accounts

Status: Phase 11 Authentication and User Accounts foundation completed; Phase 12 Dashboard V0 + Auth UI Shell completed

This document defines Sherlock's authentication and account foundation for future authenticated product usage. Sherlock will use Supabase Auth as the intended authentication provider, while keeping the current repository safe to run without a live Supabase project or real secrets.

Phase 11 is a backend/auth foundation only. Phase 12 adds static login, signup, forgot-password, and dashboard UI shells under `apps/web`. It still does not add production auth/session flow, billing, queue workers, target verification, public scan execution, report generation, PDF export, an admin panel, or production RLS policies.

## Provider Direction

Sherlock intends to use Supabase Auth for user identity.

Supabase Auth stores authentication users in the Supabase-managed `auth` schema. Sherlock app-level account metadata should live in application tables such as `public.user_profiles`, `public.organizations`, and `public.organization_members`.

The future production dashboard should prefer Supabase client-side auth for login/signup/session handling. The backend should validate Supabase-issued JWT bearer tokens before serving protected API routes.

## Current Phase 11 Backend Behavior

A live Supabase connection is optional and not required for basic local checks.

The FastAPI backend now includes:

- `GET /api/v0/auth/status` as a public configuration/status endpoint
- `GET /api/v0/me` as a protected current-user route foundation
- auth configuration placeholders for Supabase URL, anon key, service-role key, JWKS URL, and an auth enable flag
- strict bearer-token parsing helper
- auth error responses using the shared API envelope

Token validation is not production-active in Phase 11. When auth is disabled or Supabase/JWKS configuration is incomplete, protected routes return `auth_unavailable` instead of trusting fake user IDs.

## Current Phase 12 UI Behavior

The static web app now includes auth UI shell pages:

- `apps/web/login.html`
- `apps/web/signup.html`
- `apps/web/forgot-password.html`
- `apps/web/dashboard/settings.html`

These pages do not create accounts, create sessions, send password reset emails, store tokens, or store credentials. The login and settings pages may display `GET /api/v0/auth/status` when the local API is running; this endpoint returns configuration state only.

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
- Login/signup UI is implemented only as a Phase 12 static shell.
- The static web app includes public marketing pages plus a Dashboard V0 shell, not a production authenticated dashboard.
- Auth routes do not expose scanner, prompt-library, evaluator, target-verification, report-generation, billing, admin, or worker behavior.
- Production JWT validation and production RLS policies remain future reviewed work.
