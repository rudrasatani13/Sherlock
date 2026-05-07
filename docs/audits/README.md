# Manual Audit Workflow

Status: Phase 8 Manual Audit Workflow completed

This directory defines Sherlock's manual and semi-automated audit workflow for real client engagements before a full self-serve SaaS platform exists.

Sherlock is the AI Launch Security Audit + Scanner product under the PowerDetect brand. The full marketing name is **PowerDetect Sherlock**.

Naming boundary:

- Repository name: Sherlock
- Product name: Sherlock
- Brand/company identity: PowerDetect
- Marketing name: PowerDetect Sherlock
- Do not rename the repository or root folder.

## Phase 8 Scope

Phase 8 adds documentation, templates, checklists, and process guidance for human-led audits.

In scope:

- client intake workflow
- authorization and permission rules
- reusable audit scope template
- manual audit checklist
- category-specific safe manual testing playbooks
- evidence handling workflow
- finding review workflow
- severity and confidence review workflow
- report delivery workflow
- retest workflow
- audit closure workflow
- lightweight markdown templates for manual audit preparation

Out of scope:

- backend APIs
- database persistence or migrations
- authentication
- billing
- dashboard integration
- queue workers
- PDF generation
- report generation code
- public scan execution
- public self-serve scanning
- admin panel
- destructive testing automation
- unauthorized target scanning
- exploit automation beyond already-safe scanner, prompt-library, and evaluator foundations

## End-to-End Audit Flow

| Step | Workflow | Output |
| --- | --- | --- |
| 1 | Client intake | Completed intake notes and primary contact |
| 2 | Authorization | Written authorization and in-scope target list |
| 3 | Audit scoping | Approved scope, categories, windows, accounts, and forbidden actions |
| 4 | Test setup | Local scanner config, selected prompt categories, account readiness, and data-handling notes |
| 5 | Scanner execution | Local Phase 5 scanner output under ignored `scan-results/` when applicable |
| 6 | Evaluator review | Phase 7 evaluation JSON and manual-review queue when applicable |
| 7 | Manual testing | Category-specific human validation using safe playbooks |
| 8 | Evidence handling | Raw evidence protected locally and report-safe evidence redacted |
| 9 | Finding review | Deduplicated findings with category, severity, confidence, status, impact, and fix guidance |
| 10 | Report preparation | Manual report draft aligned with `docs/sample-report.md` and `docs/methodology.md` |
| 11 | Delivery | Client delivery, review meeting, limitations, and next-step agreement |
| 12 | Retesting | Fixed, still vulnerable, partially fixed, inconclusive, accepted risk, or needs manual review |
| 13 | Closure | Evidence retention/deletion, internal notes, and closed audit status |

## How Phase 5, Phase 6, and Phase 7 Fit

Phase 5 scanner engine:

- Executes controlled internal tests against authorized targets only.
- Defaults to `safe_smoke` tests and does not run the attack prompt library by default.
- Produces local JSON output under ignored `scan-results/`.
- Provides observations, not customer-facing findings.

Phase 6 prompt library:

- Provides reviewed, versioned, category-mapped test cases.
- Helps the auditor select safe scenarios by target type and methodology category.
- Supplies expected safe behavior, failure signals, severity hints, and context notes.
- Does not decide whether a target is vulnerable.

Phase 7 evaluator system:

- Consumes scanner observations and prompt metadata when present.
- Produces deterministic verdicts, severity, confidence, matched signals, evidence snippets, redacted snippets, and manual-review flags.
- Does not generate customer reports.
- Feeds the Phase 8 finding review workflow, where a human confirms impact, category, severity, confidence, and report language.

## Documentation Map

- [Client Intake Workflow](CLIENT_INTAKE.md)
- [Authorization Rules](AUTHORIZATION_RULES.md)
- [Audit Scope Template](AUDIT_SCOPE_TEMPLATE.md)
- [Manual Audit Checklist](MANUAL_AUDIT_CHECKLIST.md)
- [Category-Specific Playbooks](PLAYBOOKS.md)
- [Evidence Handling](EVIDENCE_HANDLING.md)
- [Finding Review](FINDING_REVIEW.md)
- [Severity and Confidence Review](SEVERITY_CONFIDENCE_REVIEW.md)
- [Report Delivery](REPORT_DELIVERY.md)
- [Retest Workflow](RETEST_WORKFLOW.md)
- [Audit Closure](AUDIT_CLOSURE.md)

## Optional Templates

Reusable markdown templates live under `templates/`:

- `templates/audit-intake.md`
- `templates/audit-scope.md`
- `templates/finding-review.md`
- `templates/retest-record.md`
- `templates/audit-closure.md`

Completed client copies may contain sensitive information and should not be committed to Git.

## Audit Operating Principles

- Test only systems the client owns or is explicitly authorized to test.
- Confirm written authorization before running scanner or manual tests.
- Keep target scope, test categories, and forbidden actions explicit.
- Avoid destructive actions and production impact.
- Respect rate limits, testing windows, and customer operational constraints.
- Pause testing if unexpected impact occurs.
- Use fake/demo canaries and synthetic fixtures where possible.
- Separate raw local evidence from report-safe evidence.
- Redact secrets, tokens, credentials, personal data, customer identifiers, and proprietary content.
- Never commit evidence, scan outputs, report drafts containing customer data, or completed client templates.

## Report Language Boundary

Sherlock reports should explain what was tested, what was observed, what was not tested, the evidence quality, and the limitations.

Reports must not say:

- "your AI app is secure"
- "100% protected"
- "certified safe"
- "all vulnerabilities found"
- "no risk exists"

Reports may say:

- "Sherlock tested selected categories under the stated scope."
- "Passing this audit does not guarantee complete security."
- "Manual review is recommended for high-impact findings."

## Phase 9 Readiness

Phase 8 creates the human workflow that a future product platform can model. Phase 9+ can use these documents as source material for product requirements, but should still add backend APIs, database persistence, auth, billing, dashboard surfaces, queues, report generation, PDF export, target verification, SSRF protection, and public scan controls only in explicit future phases.
