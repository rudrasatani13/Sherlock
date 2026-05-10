# Audit Scope Template

Status: Phase 8 Manual Audit Workflow

This reusable scope template defines what Sherlock will and will not test for a manual AI security audit.

Completed client scopes may contain sensitive system details. Store completed copies outside Git.

## Scope Metadata

- Client/company:
- App name:
- Audit name:
- Audit owner:
- Primary contact:
- Security escalation contact:
- Scope version:
- Date prepared:
- Date approved:
- Authorization reference:

## Target Systems

List each target separately.

| Target ID | Target name | Type | URL or interface | Owner | Notes |
| --- | --- | --- | --- | --- | --- |
| TGT-001 |  |  |  |  |  |

Target types may include:

- chatbot
- RAG assistant
- agent
- tool-using app
- support bot
- internal assistant
- customer-data-connected app
- API endpoint
- output-rendering surface

## Environments

| Environment | Included | Notes |
| --- | --- | --- |
| Pre-launch |  |  |
| Staging |  |  |
| Production |  |  |
| Demo/sandbox |  |  |

Production testing must be explicitly authorized.

## Test Accounts

| Account ID or role | Permission level | Environment | Purpose | Restrictions |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Do not include passwords, API keys, session tokens, one-time codes, private keys, or cookies in the scope document.

## Allowed Test Categories

Mark each category as allowed, not allowed, or manual-review-only.

| Category | Status | Notes |
| --- | --- | --- |
| Prompt injection |  |  |
| System prompt leakage |  |  |
| Sensitive data leakage |  |  |
| RAG data leakage / document exfiltration |  |  |
| Indirect prompt injection |  |  |
| Tool/function abuse |  |  |
| Unsafe output handling |  |  |
| Cost abuse / unbounded consumption |  |  |

## Scanner and Evaluator Use

- Phase 5 scanner mode:
- Scanner target adapter:
- Maximum scanner tests:
- Local config location:
- Output handling location:
- Phase 6 prompt-library categories selected:
- Phase 7 evaluator output location:
- Manual-review criteria:

The Phase 5 scanner is internal-only and defaults to safe smoke tests. Public self-serve scanning is not enabled.

## Forbidden Actions

List forbidden actions explicitly.

- No destructive production actions.
- No unauthorized third-party testing.
- No real customer data export.
- No credential collection.
- No payment, refund, billing, or permission-changing actions unless isolated and explicitly authorized.
- No high-volume load, spend, or stress testing unless separately authorized.

Additional client-specific forbidden actions:

-
-
-

## Testing Time Window

- Approved start:
- Approved end:
- Time zone:
- Blackout windows:
- Required notice before testing:
- Required notice after testing:
- Pause procedure:

## Rate and Usage Limits

- Maximum requests per minute:
- Maximum requests per hour:
- Maximum total prompts/requests:
- Maximum concurrency:
- Maximum model/API spend:
- Maximum test duration:
- Retry limit:
- Tool-call limit:

## Data Handling Rules

- Raw evidence storage location:
- Redacted report evidence storage location:
- Redaction requirements:
- Customer data restrictions:
- Secret/token handling:
- Screenshot handling:
- Retention period:
- Deletion owner:
- Access list:

Never commit raw evidence, scan outputs, completed client scopes, or report drafts containing client data.

## Escalation Contacts

| Contact | Role | Channel | Available during testing | Escalation reason |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Success Criteria

Define what a successful audit engagement means.

Examples:

- Selected categories tested under approved scope.
- High-impact evaluator signals manually reviewed.
- Manual playbook checks completed for applicable surfaces.
- Evidence redacted and reviewed.
- Findings deduplicated and assigned severity/confidence.
- Report delivered with tested scope, not-tested scope, limitations, and retest plan.

Client-specific success criteria:

-
-
-

## Report Expectations

- Report audience:
- Desired delivery format:
- Delivery date:
- Executive summary required:
- Engineering remediation detail required:
- Retest plan required:
- Limitations section required:
- Not-tested scope required:
- Evidence appendix allowed:
- Raw evidence excluded from report:

Reports must not claim complete security, certification, 100% protection, all vulnerabilities found, or no risk exists.

## Scope Approval

- Client approver:
- Client approver role:
- Approval date:
- Auditor approver:
- Notes:
