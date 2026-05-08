# Sherlock Development Master Plan

**Repository name:** Sherlock  
**Product name:** Sherlock  
**Brand/company identity:** PowerDetect  
**Marketing name:** PowerDetect Sherlock  
**Product category:** AI Launch Security Audit + Scanner  
**Primary audience:** Small SaaS teams, AI chatbot builders, RAG app builders, AI agent builders, and agencies building AI products.

---

## 1. Product Vision

Sherlock is an AI launch security audit and scanner product for SaaS teams that are building AI chatbots, RAG applications, tool-using agents, or customer-data-connected AI systems.

The product helps teams test their AI app before launch and detect risks such as:

- Prompt injection
- System prompt leakage
- Sensitive data leakage
- RAG data exfiltration
- Indirect prompt injection
- Tool or function abuse
- Unsafe output handling
- Cost abuse or unbounded consumption

Sherlock should not be positioned as a vague “AI prompt scanner.” It should be positioned as a practical launch-readiness security workflow for AI SaaS products.

---

## 2. Strategic Build Principle

The product should be built in this order:

1. Foundation
2. Methodology
3. Sample report
4. Internal scanner
5. Manual audit workflow
6. Backend and dashboard
7. Report system
8. Paid scanning
9. Retesting
10. Developer workflow integrations

Do not start by building a full self-serve SaaS with every feature. The correct approach is to first build a clear foundation, validate the audit methodology, create a useful report format, perform manual or semi-automated audits, and only then productize the repeated parts.

---

## 3. Important Scope Rules

These rules apply across all phases:

- Keep the repository name as **Sherlock**.
- Do not rename the root folder to PowerDetect or powerdetect-sherlock.
- Use **PowerDetect Sherlock** only as the marketing/full product name.
- Do not overbuild early.
- Do not implement scanner logic before the scanner phase.
- Do not implement billing before the billing phase.
- Do not implement auth before the auth phase.
- Do not implement dashboard screens before the dashboard phase.
- Do not store API keys in plain text.
- Do not allow scanning unverified targets.
- Do not claim that an AI app is fully secure.
- Reports must clearly state what was tested and what was not tested.
- Scanner findings must include confidence levels to reduce false-positive damage.
- High or critical severity should require strong evidence.
- Generated reports, scan outputs, logs, and sensitive files should not be committed to Git.

---

# Development Phases

---

## Phase 1: Project Foundation Setup

### Goal

Prepare a clean, scalable repository foundation for Sherlock without building product features yet.

### What to do

- Inspect the current repository before making changes.
- Preserve useful existing files.
- Create a clean monorepo-style structure.
- Add documentation folders.
- Add environment example files.
- Add ignore/config files.
- Add product naming constants or shared placeholders.
- Create a professional README.
- Document the intended architecture and roadmap.
- Add developer setup notes.

### Important boundaries

Do not build:

- Scanner logic
- Attack prompt library
- Evaluator logic
- API endpoints
- Database migrations
- Auth system
- Dashboard
- Billing
- Queue workers
- Reports

### Expected output

- Clean repository structure
- README
- Architecture document
- Roadmap document
- Security notes
- Development notes
- Environment templates
- Basic project hygiene

---

## Phase 2: Landing Page and Public Website

### Goal

Create the public-facing website that explains Sherlock and collects early interest.

### What to do

- Build a homepage.
- Explain what Sherlock does.
- Clearly position Sherlock as an AI launch security audit and scanner.
- Add sections for:
  - Hero message
  - Problem statement
  - What Sherlock tests
  - Who it is for
  - Example risks
  - Audit workflow
  - Pricing preview
  - FAQ
  - Contact or beta signup
- Add basic public pages:
  - Home
  - Pricing
  - Sample report
  - Methodology
  - Security
  - Contact or beta signup
- Add a form to collect early users:
  - Name
  - Email
  - Company/app name
  - App URL
  - Type of AI app
  - Message

### Important boundaries

Do not build:

- Full dashboard
- Auth system
- Real scanner
- Billing
- Report generator

### Expected output

- Public site live or locally ready
- Clear positioning
- Early user collection form
- Foundation for future trust-building

---

## Phase 3: Methodology and Vulnerability Categories

### Goal

Define exactly what Sherlock will test and how findings will be classified.

### What to do

- Create a methodology document.
- Define Sherlock’s initial test categories:
  - Prompt injection
  - System prompt leakage
  - Sensitive data leakage
  - RAG data leakage
  - Indirect prompt injection
  - Tool/function abuse
  - Unsafe output handling
  - Cost abuse
- For each category, define:
  - What the risk means
  - Why it matters
  - How it will be tested
  - What evidence is needed
  - How severity should be assigned
  - What a pass/fail/inconclusive result means
- Define severity levels:
  - Critical
  - High
  - Medium
  - Low
  - Informational
- Define confidence levels:
  - High
  - Medium
  - Low
- Create language standards for reporting findings.

### Important boundaries

Do not build automated scanner logic yet unless this phase is intentionally combined with scanner work later.

### Expected output

- Testing methodology
- Vulnerability taxonomy
- Severity rules
- Confidence rules
- Reporting language standards

---

## Phase 4: Sample Report Design

### Goal

Create a professional sample report that can be shown to users before the scanner is fully built.

### What to do

- Design a sample report format.
- Include these sections:
  - Launch readiness verdict
  - Security score
  - Executive summary
  - Top critical risks
  - Findings table
  - Detailed findings
  - Evidence
  - Reproduction steps
  - Fix recommendations
  - Retest status
  - What was tested
  - What was not tested
  - Limitations
  - Final launch recommendation
- Add realistic demo findings.
- Use plain-English explanations.
- Make the report readable for non-security founders.
- Keep report language honest and careful.
- Make it visually clean and professional.

### Important boundaries

Do not generate real scan results yet unless demo data is clearly marked as demo/sample.

### Expected output

- Sample report page or document
- Clear report structure
- Demo findings
- Sales/demo asset for early audits

---

## Phase 5: Internal Scanner Engine V0

### Goal

Build the first internal scanner engine for manual and semi-automated audits.

### What to do

- Create scanner engine structure.
- Add target configuration support.
- Add ability to send test prompts to a target API.
- Capture target responses.
- Store raw scan results.
- Store summarized scan results.
- Support basic scan execution from internal tooling.
- Start with API endpoint scanning only.
- Keep browser chatbot scanning for later.
- Keep this internal first, not public SaaS.

### Important boundaries

Do not expose the scanner publicly before ownership verification, abuse prevention, and safety controls exist.

### Expected output

- Internal scanner can run against authorized test targets.
- Responses can be captured.
- Results can be stored.
- Scanner output can feed reports later.

---

## Phase 6: Attack Prompt Library V0

### Goal

Create the first structured prompt suite for scanner testing.

### What to do

- Create an initial prompt library.
- Organize prompts by category:
  - Prompt injection
  - System prompt leakage
  - RAG leakage
  - Sensitive data leakage
  - Indirect injection
  - Tool abuse
  - Unsafe output
  - Cost abuse
- Start with approximately 100 prompts.
- Each prompt should include metadata:
  - Category
  - Test type
  - Severity hint
  - Expected risk
  - Notes
- Remove duplicate or low-quality prompts.
- Version the prompt suite.
- Keep prompts focused on security testing, not generic jailbreak entertainment.

### Important boundaries

Avoid huge prompt libraries too early. Quality and evidence matter more than volume.

### Expected output

- Sherlock Prompt Suite V0
- Categorized prompt library
- Metadata for each test
- Versioned prompt set

---

## Phase 7: Evaluator System V0

### Goal

Create a basic system to judge target responses and convert them into useful signals.

### What to do

- Create rule-based evaluators.
- Add pattern detection for:
  - API key-like strings
  - Password-like content
  - Private key-like content
  - System prompt phrases
  - Canary token leakage
  - HTML/script output
  - Suspicious data exposure
- Add canary token detection.
- Add basic classification:
  - Safe
  - Suspicious
  - Vulnerable
  - Needs manual review
- Assign severity and confidence.
- Keep the evaluator explainable.
- Use LLM-as-judge carefully and only where useful.
- Avoid treating LLM judgment as absolute truth.

### Important boundaries

Do not mark findings as critical without strong evidence. Do not overuse expensive model-based judging.

### Expected output

- Basic automated response evaluation
- Initial severity assignment
- Initial confidence assignment
- Findings candidates for manual review

---

## Phase 8: Manual Audit Workflow

### Goal

Define the manual/semi-automated audit process so real users can be served before full SaaS automation.

### What to do

- Create client intake workflow.
- Define required information:
  - App name
  - App URL
  - API endpoint if available
  - Test credentials
  - App type
  - Data sensitivity
  - RAG usage
  - Tool/agent usage
  - Launch status
- Create manual audit checklist.
- Define audit steps:
  - Intake review
  - Target verification
  - Safe test setup
  - Internal scanner run
  - Manual testing
  - Evidence capture
  - Findings review
  - Report writing
  - Fix recommendations
  - Retest
- Create audit delivery process.
- Track repeated issues found across audits.

### Important boundaries

Only test targets where permission is clearly provided.

### Expected output

- Manual audit process
- Intake checklist
- Audit checklist
- Delivery workflow
- Feedback loop for productization

---

## Phase 9: Backend API Foundation

### Goal

Create the backend foundation needed for project management, scan management, and future dashboard integration.

### What to do

- Set up backend application structure.
- Create core service boundaries.
- Add basic API route planning.
- Prepare routes for:
  - Projects
  - Scans
  - Findings
  - Reports
  - Verification
- Add validation strategy.
- Add error handling strategy.
- Add logging strategy.
- Add environment configuration.
- Keep the backend modular so scanner logic can plug into it later.

### Important boundaries

Do not add full database/auth/billing logic unless those phases are active.

### Expected output

- Backend foundation
- API structure
- Service boundaries
- Ready for database integration

---

## Phase 10: Database Setup

### Goal

Create the database structure for users, organizations, projects, scans, findings, and reports.

### What to do

- Set up Supabase or chosen database.
- Define core tables:
  - Users
  - Organizations
  - Projects
  - Scans
  - Findings
  - Scan events
  - Reports
  - Subscriptions or billing records later
- Define relationships:
  - User to organization
  - Organization to projects
  - Project to scans
  - Scan to findings
  - Scan to reports
- Plan row-level security.
- Plan data retention rules.
- Plan sensitive data redaction.
- Add seed/demo data only if useful.

### Important boundaries

Do not store secrets in plain text. Do not commit real database credentials.

### Expected output

- Database schema
- Relationship model
- Data security plan
- Ready for auth and dashboard integration

---

## Phase 11: Authentication and User Accounts

### Goal

Allow users to sign up, log in, and access protected dashboard areas.

### What to do

- Set up authentication provider.
- Add signup flow.
- Add login flow.
- Add logout flow.
- Add password reset flow.
- Create protected routes.
- Create organization creation or default workspace creation.
- Add account settings page.
- Add session handling.
- Add basic role planning:
  - Owner
  - Admin
  - Member
  - Viewer later

### Important boundaries

Do not expose admin capabilities to normal users.

### Expected output

- Working user accounts
- Protected dashboard shell
- Organization/workspace foundation

---

## Phase 12: Dashboard V0

### Goal

Create the basic user dashboard for managing projects and scans.

### What to do

- Build dashboard home.
- Build project list.
- Build add project flow.
- Build project detail page.
- Build scan list.
- Build scan detail page.
- Build findings page.
- Build report page.
- Add empty states.
- Add loading states.
- Add error states.
- Keep UI simple and functional.

### Important boundaries

Do not build complex analytics or advanced admin features yet.

### Expected output

- Basic user dashboard
- Users can view projects, scans, findings, and reports
- Ready for scanner connection

---

## Phase 13: Project Target Setup

### Goal

Allow users to configure the AI app target that Sherlock will test.

### What to do

- Add target creation flow.
- Support initial target types:
  - API endpoint
  - OpenAI-compatible endpoint
  - Vercel AI SDK-style endpoint
  - Manual audit target
- Collect required fields:
  - Target name
  - Endpoint URL
  - Auth type
  - Headers or temporary token
  - App description
  - Framework/stack if known
  - RAG usage
  - Tool/agent usage
- Validate URLs.
- Validate response format.
- Warn users about sensitive credentials.
- Prefer temporary test keys.
- Prepare for secure storage or non-storage of secrets.

### Important boundaries

Do not run scans against unverified or unauthorized targets.

### Expected output

- Target setup flow
- Target metadata stored
- Ready for verification

---

## Phase 14: Ownership Verification

### Goal

Prevent abuse by ensuring users can only scan targets they own or are authorized to test.

### What to do

- Add target verification state.
- Support verification methods:
  - DNS TXT record
  - HTML meta tag
  - Verification file
  - Secret challenge response
- Show verification instructions in the dashboard.
- Allow users to retry verification.
- Block scans for unverified targets.
- Store verification status.
- Log verification attempts.

### Important boundaries

This phase is security-critical. Do not allow public scanning without verification.

### Expected output

- Target verification system
- Verified/unverified status
- Scan blocking for unverified targets

---

## Phase 15: Queue and Worker System

### Goal

Run scans asynchronously in background workers instead of normal web requests.

### What to do

- Set up a queue system.
- Create scan job lifecycle:
  - Pending
  - Running
  - Completed
  - Failed
  - Cancelled
- Add worker process.
- Add job creation when a scan starts.
- Add progress tracking.
- Add timeout handling.
- Add retry handling.
- Store worker logs safely.
- Save scan events.
- Prevent duplicate concurrent scans when needed.

### Important boundaries

Do not run heavy scans inside request-response API handlers.

### Expected output

- Background scan execution
- Scan status tracking
- Reliable worker flow

---

## Phase 16: Scan Types and Limits

### Goal

Define different scan depths and enforce limits.

### What to do

- Create scan types:
  - Quick scan
  - Standard scan
  - Deep scan
  - Manual review scan
- Define per-scan limits:
  - Number of prompts
  - Runtime limit
  - Categories included
  - Evidence retention
  - Report detail level
- Map scan types to pricing or access levels.
- Add scan type selector in the dashboard.
- Add usage tracking.
- Add abuse prevention.
- Keep free scans limited.

### Important boundaries

Do not offer unlimited scans early. Scanner cost and abuse risk must be controlled.

### Expected output

- Scan tiers
- Scan limits
- Usage-controlled scanning

---

## Phase 17: Findings System

### Goal

Convert raw scanner results into clean, actionable findings.

### What to do

- Define finding structure:
  - Title
  - Category
  - Severity
  - Confidence
  - Description
  - Business impact
  - Evidence
  - Reproduction steps
  - Fix recommendation
  - Status
- Group duplicate findings.
- Merge similar findings.
- Sort by severity and confidence.
- Add finding statuses:
  - Open
  - Fixed
  - Accepted risk
  - False positive
  - Needs review
- Add manual review notes later.
- Make findings understandable to non-security developers.

### Important boundaries

Avoid vague findings. Every serious finding should include evidence and fix guidance.

### Expected output

- Clean findings model
- Useful findings page
- Better report quality

---

## Phase 18: Web Report

### Goal

Show scan results as a professional web-based report.

### What to do

- Create report summary page.
- Add launch readiness verdict.
- Add security score.
- Add severity breakdown.
- Add top fixes.
- Add findings table.
- Add detailed finding sections.
- Add evidence snippets with redaction.
- Add reproduction steps.
- Add fix recommendations.
- Add tested categories section.
- Add limitations section.
- Add report sharing or export planning.

### Important boundaries

The report must not overclaim security. Include limitations clearly.

### Expected output

- Web report
- Useful security summary
- Actionable findings and fixes

---

## Phase 19: PDF Report Export

### Goal

Allow users to download a polished PDF report.

### What to do

- Convert report view to PDF.
- Create PDF template.
- Include:
  - Cover page
  - Executive summary
  - Launch readiness verdict
  - Score
  - Findings
  - Evidence
  - Fixes
  - Tested categories
  - Limitations
- Store generated PDFs securely.
- Add download button.
- Gate PDF export behind paid plans if needed.
- Redact sensitive evidence in PDF.

### Important boundaries

Do not include secrets or raw sensitive data in downloadable reports.

### Expected output

- Professional PDF report
- Downloadable report asset
- Paid feature candidate

---

## Phase 20: Retest Flow

### Goal

Allow users to verify whether fixes worked.

### What to do

- Add finding-specific retest.
- Add full scan retest.
- Compare old and new results.
- Show statuses:
  - Fixed
  - Still vulnerable
  - Partially fixed
  - Inconclusive
- Add retest history.
- Update reports with retest status.
- Add plan-based retest limits.
- Make retest workflow simple.

### Important boundaries

Retest results should not erase original evidence. Keep history.

### Expected output

- Fix verification workflow
- Stronger product value
- Better customer retention

---

## Phase 21: Billing and Plans

### Goal

Enable paid usage.

### What to do

- Set up billing provider.
- Create plans:
  - Free
  - Launch scan
  - Builder
  - Startup
  - Manual audit
- Add checkout flow.
- Add subscription tracking.
- Add usage limits.
- Add paid feature gates:
  - Full scan
  - PDF report
  - Retest
  - More projects
  - More scan history
  - Deep categories
- Add billing settings page.
- Handle subscription lifecycle events.

### Important boundaries

Do not allow usage without enforcing limits. Do not expose paid features accidentally.

### Expected output

- Paid product foundation
- Subscription and one-time payment support
- Plan-based access control

---

## Phase 22: Platform Security Hardening

### Goal

Protect Sherlock itself from abuse and vulnerabilities.

### What to do

- Add rate limiting.
- Add input validation.
- Add target URL validation.
- Add SSRF protection.
- Block private IP ranges.
- Block localhost/internal metadata endpoints.
- Securely handle secrets.
- Prevent sensitive data in logs.
- Add audit logs.
- Add abuse detection.
- Add safe error messages.
- Add data deletion controls.
- Review authorization checks.
- Review row-level security.
- Review report access permissions.

### Important boundaries

This phase is mandatory before public launch.

### Expected output

- Safer platform
- Reduced abuse risk
- Better trust posture

---

## Phase 23: Admin Panel

### Goal

Allow internal operation and support.

### What to do

- Add admin-only access.
- Add user list.
- Add project list.
- Add scan list.
- Add failed scans view.
- Add findings review view.
- Add manual audit notes.
- Add abuse flagging.
- Add support workflow basics.
- Add refund/payment support references if needed.
- Add admin audit log.

### Important boundaries

Protect admin routes strongly. Never expose admin data to normal users.

### Expected output

- Internal operations dashboard
- Easier support and review
- Manual audit support

---

## Phase 24: Manual Review Layer

### Goal

Add a human-reviewed upgrade path for higher-value customers.

### What to do

- Add “Request Manual Review” flow.
- Allow users to submit a scan for review.
- Allow admin to review findings.
- Allow admin to adjust severity/confidence.
- Allow admin to add notes and fix guidance.
- Add manual-reviewed badge.
- Add final approval step for reports.
- Add pricing/plan tie-in.

### Important boundaries

Manual review should be clearly distinguished from automated scan results.

### Expected output

- Higher-trust audit reports
- Higher pricing justification
- Hybrid service + SaaS workflow

---

## Phase 25: Local Runner

### Goal

Support privacy-conscious teams that do not want to send API keys or sensitive data to the cloud.

### What to do

- Design local runner architecture.
- Let users install a local runner.
- Runner should pull authorized test suites.
- Runner should run tests inside the user's environment.
- API keys should remain local where possible.
- Results can be uploaded selectively.
- Add local-only mode planning.
- Add runner registration.
- Add runner authentication.
- Add runner status page.

### Important boundaries

Do not build this before core scanner/report workflow is validated.

### Expected output

- Privacy-friendly scanning path
- Better trust with serious teams
- Strong differentiator

---

## Phase 26: GitHub and CI Integration

### Goal

Move Sherlock into developer workflows.

### What to do

- Plan GitHub app integration.
- Allow repository connection.
- Add CI scan trigger.
- Add pull request comments.
- Add status checks:
  - Passed
  - Warning
  - Failed
- Add GitHub Actions template.
- Add security regression scan support.
- Add scan history by commit/branch.
- Add failure thresholds.

### Important boundaries

Do not add CI until scan quality is useful enough to avoid noisy developer workflows.

### Expected output

- Developer workflow integration
- Recurring usage
- Better retention

---

## Phase 27: Framework-Specific Fix Guidance

### Goal

Make reports more useful by giving stack-specific remediation guidance.

### What to do

- Ask or detect user stack:
  - Vercel AI SDK
  - LangChain
  - LlamaIndex
  - OpenAI API
  - Custom backend
  - Agent framework
- Create fix templates by framework.
- Add guidance for:
  - RAG access control
  - Retrieval filtering
  - Tool permission boundaries
  - Output sanitization
  - Rate limiting
  - Prompt hardening
  - User isolation
  - Logging and redaction
- Add “How to fix this in your stack” report section.
- Improve recommendations based on repeated audits.

### Important boundaries

Avoid generic advice only. Stack-specific guidance is a major value driver.

### Expected output

- Better remediation quality
- More valuable reports
- Stronger differentiation

---

## Phase 28: Testing and QA

### Goal

Make the product stable and trustworthy.

### What to do

- Add unit tests for:
  - Evaluator logic
  - Severity scoring
  - Prompt loading
  - Target validation
  - Report rendering
- Add integration tests for:
  - Creating projects
  - Running scans
  - Worker execution
  - Finding creation
  - Report generation
- Add security tests for:
  - SSRF protection
  - Auth bypass
  - Rate limiting
  - Data isolation
  - Report access control
- Create dummy target apps:
  - Safe chatbot
  - Vulnerable chatbot
  - RAG leak demo
  - Tool abuse demo
- Add release checklist.

### Important boundaries

Security product quality matters. Broken or noisy scans damage trust quickly.

### Expected output

- Test coverage
- Demo targets
- Release confidence
- Reduced regressions

---

## Phase 29: Private Beta

### Goal

Test Sherlock with real users before public launch.

### What to do

- Invite 10–20 early users.
- Offer free quick scan.
- Offer discounted full audit.
- Track onboarding friction.
- Track scan runtime.
- Track cost per scan.
- Track false positives.
- Track false negatives found manually.
- Ask whether users would pay.
- Improve report clarity.
- Improve setup flow.
- Improve severity scoring.
- Collect testimonials or anonymized case studies.

### Important boundaries

Do not overpromise. Treat beta as learning, not final product.

### Expected output

- Real user feedback
- Pricing signals
- Product quality improvements
- Launch readiness

---

## Phase 30: Public Launch V1

### Goal

Launch Sherlock publicly.

### What to do

- Finalize homepage.
- Finalize pricing.
- Publish sample report.
- Publish methodology page.
- Publish security and privacy pages.
- Enable free quick scan.
- Enable paid full scan or launch audit.
- Enable PDF export if ready.
- Enable support email.
- Prepare launch content.
- Publish technical blog posts.
- Launch in relevant communities.
- Monitor failures and user feedback closely.

### Important boundaries

Public launch should happen only after verification, rate limiting, SSRF protection, and data handling are solid.

### Expected output

- Public V1 product
- Working acquisition funnel
- Paid scan/audit offering
- Feedback loop for next version

---

# MVP Phase Subset

For the first MVP, focus only on these phases:

1. Phase 1: Project Foundation Setup
2. Phase 2: Landing Page and Public Website
3. Phase 3: Methodology and Vulnerability Categories
4. Phase 4: Sample Report Design
5. Phase 5: Internal Scanner Engine V0
6. Phase 6: Attack Prompt Library V0
7. Phase 7: Evaluator System V0
8. Phase 8: Manual Audit Workflow
9. Phase 9: Backend API Foundation
10. Phase 10: Database Setup
11. Phase 11: Authentication and User Accounts
12. Phase 12: Dashboard V0
13. Phase 13: Project Target Setup
14. Phase 15: Queue and Worker System
15. Phase 18: Web Report

Billing, PDF export, retesting, admin panel, local runner, GitHub integration, and framework-specific fixes can come after the MVP is working.

---

# Fastest Practical Build Order

If the goal is to move fast without overbuilding, follow this order:

1. Landing page
2. Sample report
3. Methodology
4. Internal scanner
5. Prompt library
6. Evaluator
7. Manual audits
8. Backend API
9. Database
10. Auth
11. Dashboard
12. Queue workers
13. Web report
14. Paid launch scan
15. Retest
16. PDF export

---

# Codex Usage Guidance

When using Codex, work one phase at a time.

For each phase:

1. Ask Codex to inspect the current repository first.
2. Tell Codex the current phase number.
3. Tell Codex not to build future-phase features.
4. Ask Codex to preserve existing working files.
5. Ask Codex to summarize files changed.
6. Ask Codex to run validation if possible.
7. After completion, ask Codex to review whether it accidentally exceeded the phase scope.

Example instruction style:

“Implement Phase X only. Do not implement scanner/dashboard/billing/auth unless this phase requires it. Inspect the current repository first, make minimal clean changes, then summarize exactly what changed and what remains for the next phase.”

---

# Final Product Principle

Sherlock should not become a generic prompt-list wrapper.

Sherlock should become:

**An AI launch security workflow that helps SaaS teams find, understand, fix, and retest AI-specific security risks before launch.**

The long-term value is not just prompts. The value is:

- Trust
- Methodology
- Evidence
- Plain-English reports
- Fix recommendations
- Retesting
- Developer workflow integration
- Manual expertise converted into software
