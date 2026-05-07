# Project Overview

Sherlock is an AI Launch Security Audit + Scanner product under the PowerDetect brand.

The product name is **Sherlock**. The full marketing name is **PowerDetect Sherlock**.

Sherlock will help SaaS teams test AI chatbots, RAG systems, tool-using agents, and customer-data-connected AI applications before launch.

## Product Category

AI Launch Security Audit + Scanner

## Intended Users

Sherlock is intended for SaaS founders, engineering teams, security teams, and product teams preparing to launch AI features that interact with users, private data, tools, or internal systems.

## Future Risk Areas

Sherlock will later test for:

- prompt injection
- system prompt leakage
- sensitive data leakage
- RAG data exfiltration
- indirect prompt injection
- tool/function abuse
- unsafe output handling
- cost abuse and unbounded consumption

## Current Phase

Current phase: **Phase 11 Authentication and User Accounts foundation completed**

Phase 1 established repository organization, documentation, environment templates, security notes, roadmap notes, and basic hygiene.

Phase 2 adds a static public website under `apps/web` with product positioning, a homepage, sample report page, public methodology page, security/trust page, pricing and early-access page, and contact/beta/audit request UI.

Phase 3 adds the internal methodology foundation, vulnerability category taxonomy, evidence standards, severity model, confidence model, finding status definitions, report language standards, and guidance for later prompt, evaluator, scanner, report, and manual audit phases.

Phase 4 expands the public sample report into a polished static demo artifact and adds an internal sample report reference document with reusable report content structure, fictional findings, sanitized evidence rules, retest language, limitations, and disclaimer guidance.

Phase 5 adds the internal scanner engine foundation under `packages/scanner_engine` with target configuration, target adapters, safe smoke tests, scan lifecycle state, and local JSON outputs.

Phase 6 adds the internal attack prompt/test-case library under `packages/prompt_library` with a manifest, schema reference, category files, safe metadata, loader utilities, validation utilities, and scanner conversion helpers.

Phase 7 adds the internal evaluator system under `packages/evaluator_system` with deterministic rule-based detectors, structured evaluation results, evidence redaction helpers, a local CLI, and unittest coverage.

Phase 8 adds the manual and semi-automated audit workflow under `docs/audits` with intake, authorization, scoping, test setup, scanner execution guidance, evaluator review, manual playbooks, evidence handling, finding review, report delivery, retesting, audit closure, and lightweight templates under `templates`.

Phase 9 adds a minimal backend API foundation under `apps/api` with FastAPI health and version/status endpoints, placeholder route modules, config loading, logging, CORS placeholder, response schemas, structured error handling, and lightweight tests.

Phase 10 adds a PostgreSQL/Supabase-compatible database foundation under `db/` with schema documentation, an initial migration, local setup notes, RLS planning, and privacy/security boundaries.

Phase 11 adds a Supabase Auth-compatible authentication and user account foundation with safe configuration placeholders, backend auth helpers, auth status and current-user route placeholders, account model documentation, and tests.

Authenticated dashboard, production login/signup UI, production JWT verification, active API database persistence, billing, queue workers, public scan execution, target verification implementation, admin panel, PDF generation, real report generation, and public scanner execution are still not implemented.

## Product Principle

Sherlock should communicate evidence and risk clearly. It should not make absolute claims that a customer's AI application is secure.
