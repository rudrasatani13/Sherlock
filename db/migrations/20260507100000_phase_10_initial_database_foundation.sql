BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

CREATE TYPE public.organization_status AS ENUM ('active', 'trial', 'suspended', 'archived');
CREATE TYPE public.organization_member_role AS ENUM ('owner', 'admin', 'member', 'viewer');
CREATE TYPE public.project_environment AS ENUM ('development', 'staging', 'production', 'demo', 'other');
CREATE TYPE public.project_status AS ENUM ('draft', 'active', 'archived');
CREATE TYPE public.target_type AS ENUM ('api_endpoint', 'openai_compatible', 'vercel_ai_sdk', 'langchain', 'llamaindex', 'chatbot_url', 'manual');
CREATE TYPE public.target_auth_type AS ENUM ('none', 'api_key', 'bearer_token', 'basic', 'custom', 'future_secret_reference');
CREATE TYPE public.target_verification_status AS ENUM ('pending', 'verified', 'failed', 'expired');
CREATE TYPE public.scan_type AS ENUM ('quick', 'standard', 'deep', 'manual');
CREATE TYPE public.scan_status AS ENUM ('pending', 'running', 'completed', 'failed', 'cancelled');
CREATE TYPE public.finding_severity AS ENUM ('critical', 'high', 'medium', 'low', 'informational');
CREATE TYPE public.finding_confidence AS ENUM ('high', 'medium', 'low');
CREATE TYPE public.finding_status AS ENUM ('open', 'fixed', 'accepted_risk', 'false_positive', 'needs_manual_review', 'inconclusive');
CREATE TYPE public.report_status AS ENUM ('draft', 'ready', 'delivered', 'archived', 'failed');
CREATE TYPE public.manual_audit_status AS ENUM ('draft', 'scoped', 'authorized', 'in_progress', 'delivered', 'closed', 'cancelled');
CREATE TYPE public.audit_authorization_status AS ENUM ('pending', 'authorized', 'expired', 'revoked', 'not_required');
CREATE TYPE public.retest_status AS ENUM ('fixed', 'still_vulnerable', 'partially_fixed', 'inconclusive', 'accepted_risk', 'needs_manual_review');

CREATE TABLE public.organizations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    slug text NOT NULL UNIQUE,
    plan text NOT NULL DEFAULT 'starter',
    status public.organization_status NOT NULL DEFAULT 'trial',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(name)) > 0),
    CHECK (slug ~ '^[a-z0-9][a-z0-9-]*[a-z0-9]$' OR slug ~ '^[a-z0-9]$')
);

CREATE TABLE public.user_profiles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text UNIQUE,
    display_name text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (email IS NULL OR position('@' in email) > 1)
);

CREATE TABLE public.organization_members (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,
    role public.organization_member_role NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (organization_id, user_id)
);

CREATE TABLE public.projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    name text NOT NULL,
    description text,
    app_type text,
    environment public.project_environment NOT NULL DEFAULT 'staging',
    status public.project_status NOT NULL DEFAULT 'draft',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(name)) > 0)
);

CREATE TABLE public.targets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    target_type public.target_type NOT NULL,
    name text NOT NULL,
    url text,
    method text NOT NULL DEFAULT 'POST' CHECK (method IN ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')),
    auth_type public.target_auth_type NOT NULL DEFAULT 'none',
    safe_metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    is_verified boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(name)) > 0),
    CHECK (url IS NULL OR url ~* '^https?://')
);

CREATE TABLE public.target_verifications (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id uuid NOT NULL REFERENCES public.targets(id) ON DELETE CASCADE,
    verification_type text NOT NULL,
    status public.target_verification_status NOT NULL DEFAULT 'pending',
    challenge_hash text,
    challenge_reference text,
    verified_at timestamptz,
    expires_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(verification_type)) > 0)
);

CREATE TABLE public.scans (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    target_id uuid REFERENCES public.targets(id) ON DELETE SET NULL,
    scan_type public.scan_type NOT NULL,
    status public.scan_status NOT NULL DEFAULT 'pending',
    started_at timestamptz,
    completed_at timestamptz,
    summary jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (completed_at IS NULL OR started_at IS NULL OR completed_at >= started_at)
);

CREATE TABLE public.scan_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id uuid NOT NULL REFERENCES public.scans(id) ON DELETE CASCADE,
    event_type text NOT NULL,
    message text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(event_type)) > 0)
);

CREATE TABLE public.findings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id uuid REFERENCES public.scans(id) ON DELETE SET NULL,
    project_id uuid NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    category text NOT NULL,
    title text NOT NULL,
    severity public.finding_severity NOT NULL,
    confidence public.finding_confidence NOT NULL,
    status public.finding_status NOT NULL DEFAULT 'needs_manual_review',
    description text,
    business_impact text,
    evidence_summary text,
    recommendation text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(category)) > 0),
    CHECK (length(trim(title)) > 0)
);

CREATE TABLE public.reports (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id uuid REFERENCES public.scans(id) ON DELETE SET NULL,
    project_id uuid NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    report_type text NOT NULL DEFAULT 'launch_security_audit',
    status public.report_status NOT NULL DEFAULT 'draft',
    storage_path text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(report_type)) > 0)
);

CREATE TABLE public.manual_audits (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    project_id uuid REFERENCES public.projects(id) ON DELETE SET NULL,
    status public.manual_audit_status NOT NULL DEFAULT 'draft',
    scope_summary text,
    authorization_status public.audit_authorization_status NOT NULL DEFAULT 'pending',
    started_at timestamptz,
    completed_at timestamptz,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (completed_at IS NULL OR started_at IS NULL OR completed_at >= started_at)
);

CREATE TABLE public.retests (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    finding_id uuid REFERENCES public.findings(id) ON DELETE CASCADE,
    scan_id uuid REFERENCES public.scans(id) ON DELETE SET NULL,
    status public.retest_status NOT NULL,
    notes text,
    retested_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (finding_id IS NOT NULL OR scan_id IS NOT NULL)
);

CREATE TABLE public.usage_records (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    usage_type text NOT NULL,
    quantity numeric(12, 2) NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    period_start timestamptz,
    period_end timestamptz,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(usage_type)) > 0),
    CHECK (period_end IS NULL OR period_start IS NULL OR period_end >= period_start)
);

CREATE TABLE public.audit_logs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid REFERENCES public.organizations(id) ON DELETE SET NULL,
    actor_user_id uuid REFERENCES public.user_profiles(id) ON DELETE SET NULL,
    action text NOT NULL,
    entity_type text NOT NULL,
    entity_id uuid,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(action)) > 0),
    CHECK (length(trim(entity_type)) > 0)
);

CREATE INDEX idx_organization_members_organization_id ON public.organization_members(organization_id);
CREATE INDEX idx_organization_members_user_id ON public.organization_members(user_id);
CREATE INDEX idx_projects_organization_id ON public.projects(organization_id);
CREATE INDEX idx_targets_project_id ON public.targets(project_id);
CREATE INDEX idx_target_verifications_target_id ON public.target_verifications(target_id);
CREATE INDEX idx_scans_project_id ON public.scans(project_id);
CREATE INDEX idx_scans_target_id ON public.scans(target_id);
CREATE INDEX idx_scan_events_scan_id_created_at ON public.scan_events(scan_id, created_at);
CREATE INDEX idx_findings_project_id ON public.findings(project_id);
CREATE INDEX idx_findings_scan_id ON public.findings(scan_id);
CREATE INDEX idx_findings_status ON public.findings(status);
CREATE INDEX idx_reports_project_id ON public.reports(project_id);
CREATE INDEX idx_reports_scan_id ON public.reports(scan_id);
CREATE INDEX idx_manual_audits_organization_id ON public.manual_audits(organization_id);
CREATE INDEX idx_manual_audits_project_id ON public.manual_audits(project_id);
CREATE INDEX idx_retests_finding_id ON public.retests(finding_id);
CREATE INDEX idx_retests_scan_id ON public.retests(scan_id);
CREATE INDEX idx_usage_records_organization_id ON public.usage_records(organization_id);
CREATE INDEX idx_audit_logs_organization_id_created_at ON public.audit_logs(organization_id, created_at);
CREATE INDEX idx_audit_logs_actor_user_id ON public.audit_logs(actor_user_id);

CREATE TRIGGER set_organizations_updated_at
BEFORE UPDATE ON public.organizations
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_user_profiles_updated_at
BEFORE UPDATE ON public.user_profiles
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_projects_updated_at
BEFORE UPDATE ON public.projects
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_targets_updated_at
BEFORE UPDATE ON public.targets
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_scans_updated_at
BEFORE UPDATE ON public.scans
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_findings_updated_at
BEFORE UPDATE ON public.findings
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_reports_updated_at
BEFORE UPDATE ON public.reports
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_manual_audits_updated_at
BEFORE UPDATE ON public.manual_audits
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organization_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.targets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.target_verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scan_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.findings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.manual_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.retests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

COMMENT ON TABLE public.organizations IS 'Phase 10 workspace/team/company containers. RLS enabled; no user policies until auth is implemented.';
COMMENT ON TABLE public.user_profiles IS 'Phase 10 app-level user metadata placeholder. Future Supabase Auth integration should connect id to auth.users.id.';
COMMENT ON TABLE public.organization_members IS 'Phase 10 future organization membership and roles. No auth flows are implemented.';
COMMENT ON TABLE public.projects IS 'Phase 10 AI app/project metadata. Not connected to public API persistence yet.';
COMMENT ON TABLE public.targets IS 'Phase 10 target metadata only. Do not store plaintext secrets, raw headers, cookies, or tokens.';
COMMENT ON TABLE public.target_verifications IS 'Phase 10 future ownership verification records. Verification logic is not implemented.';
COMMENT ON TABLE public.scans IS 'Phase 10 scan job metadata. Public scan execution, queues, and scanner persistence are not implemented.';
COMMENT ON TABLE public.scan_events IS 'Phase 10 scan lifecycle timeline foundation. Avoid raw sensitive evidence by default.';
COMMENT ON TABLE public.findings IS 'Phase 10 reviewed finding metadata foundation. Evidence summaries should be report-safe and redacted.';
COMMENT ON TABLE public.reports IS 'Phase 10 report metadata placeholder. Report generation and PDF export are not implemented.';
COMMENT ON TABLE public.manual_audits IS 'Phase 10 manual audit engagement records based on Phase 8 workflow. Store sensitive client records outside Git.';
COMMENT ON TABLE public.retests IS 'Phase 10 retest tracking records for future finding and scan retests.';
COMMENT ON TABLE public.usage_records IS 'Phase 10 future usage/billing foundation. Billing integration is not implemented.';
COMMENT ON TABLE public.audit_logs IS 'Phase 10 future security audit log foundation. Write paths and review workflows are future work.';
COMMENT ON COLUMN public.targets.safe_metadata IS 'Safe metadata only. Do not store plaintext credentials, API keys, tokens, cookies, passwords, private keys, or raw auth headers.';
COMMENT ON COLUMN public.findings.evidence_summary IS 'Report-safe redacted evidence summary only. Raw evidence should not be stored by default.';
COMMENT ON COLUMN public.reports.storage_path IS 'Placeholder for future report storage reference. No report generation or storage integration exists in Phase 10.';

COMMIT;
