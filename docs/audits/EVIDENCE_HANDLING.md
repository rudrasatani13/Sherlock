# Evidence Handling Workflow

Status: Phase 8 Manual Audit Workflow

Evidence handling controls how Sherlock auditors collect, protect, redact, summarize, retain, and delete audit evidence.

Evidence may contain sensitive prompts, model responses, retrieval traces, tool logs, screenshots, headers, account identifiers, or customer context. Never commit evidence or scan outputs to Git.

## Evidence Goals

- Preserve enough information to support reproducible findings.
- Minimize sensitive data collection.
- Redact secrets and customer data before report delivery.
- Separate raw local evidence from redacted report evidence.
- Keep access limited to authorized audit participants.
- Define retention and deletion expectations before delivery.

## Evidence Types

Potential evidence includes:

- scanner output JSON under ignored `scan-results/`
- Phase 7 evaluation JSON under ignored `scan-results/evaluations/`
- short model output excerpts
- prompt-library test IDs or scenario IDs
- screenshots
- tool traces or action logs
- retrieval source IDs or citation metadata
- sanitized reproduction summaries
- client confirmation notes
- manual review decisions
- retest records

## Collection Rules

- Keep snippets short.
- Capture only what is needed to support the finding.
- Prefer identifiers, summaries, and redacted excerpts over long raw transcripts.
- Use fake/demo canaries where possible.
- Mark demo/canary values clearly.
- Do not include real customer data in examples.
- Do not store unnecessary raw outputs.
- Avoid storing full prompts, full responses, headers, cookies, uploaded files, or source documents unless explicitly needed and authorized.
- Stop and escalate if credentials, tokens, private keys, passwords, session cookies, one-time codes, regulated data, or unexpected real customer data appears.

## Redaction Rules

Redact:

- API keys
- access tokens
- refresh tokens
- bearer tokens
- passwords
- private keys
- session identifiers
- cookies
- webhook secrets
- customer identifiers
- personal data
- account, billing, support, health, financial, or compliance data
- internal hostnames where sensitive
- proprietary document text that is not required for remediation

Use placeholders such as:

- `[REDACTED_TOKEN]`
- `[REDACTED_SECRET]`
- `[REDACTED_CUSTOMER_ID]`
- `[REDACTED_EMAIL]`
- `[REDACTED_PRIVATE_DOCUMENT]`
- `[DEMO_CANARY]`

Do not replace real secrets with fake realistic secrets that could be mistaken for live credentials.

## Raw Evidence vs Report-Safe Evidence

### Raw Evidence

Raw evidence is the protected local material used for internal validation.

Examples:

- full local scanner output
- full local evaluator output
- unredacted screenshots
- complete tool traces
- complete retrieval traces

Rules:

- Store outside Git or in ignored paths.
- Restrict access to authorized audit participants.
- Apply client retention requirements.
- Delete when no longer needed or when required by agreement.
- Do not deliver raw evidence unless explicitly approved.

### Report-Safe Evidence

Redacted report evidence is what may appear in the final audit report.

Examples:

- short redacted snippets
- summarized behavior
- synthetic canary references
- screenshot crops with sensitive data removed
- tool/action summaries with arguments redacted
- retrieval source summaries without private content

Rules:

- Use the minimum detail needed for remediation.
- Include enough context to explain impact and retest steps.
- Avoid raw attack prompts unless explicitly approved.
- Avoid real customer data and long transcripts.
- Include redaction notes when relevant.

## Evidence Review Workflow

1. Identify candidate evidence from scanner, evaluator, and manual testing.
2. Classify it as raw evidence or redacted report evidence.
3. Remove unnecessary raw outputs.
4. Redact secrets, credentials, tokens, personal data, and customer identifiers.
5. Confirm demo/canary values are clearly labeled.
6. Confirm the evidence supports category, severity, confidence, and business impact.
7. Ask the client to confirm sensitivity or permissions when ambiguous.
8. Store raw evidence in the protected location.
9. Move only redacted excerpts into the finding draft.
10. Re-check the final report for over-disclosure before delivery.

## Access Rules

Evidence access should be limited to:

- assigned auditor or audit team
- client-approved security or engineering contacts
- reviewers needed for quality control
- legal or compliance contacts only when required by the engagement

Do not share evidence through public links, issue trackers, chat channels, or repositories unless the client has approved the channel and access controls.

## Retention and Deletion

Before testing, record:

- raw evidence storage location
- redacted report evidence storage location
- access list
- retention period
- deletion date or trigger
- deletion owner
- whether client requires evidence handoff or destruction confirmation

At closure:

- review raw evidence still stored
- delete material no longer needed
- retain only what the agreement permits
- document deletion or retention decisions
- confirm no evidence was committed to Git

## Git and Local Artifact Rules

Never commit:

- `scan-results/`
- evaluator outputs
- raw evidence
- screenshots containing client data
- completed intake, scope, finding, retest, or closure templates containing client data
- report drafts containing client data
- authorization records
- credentials or environment files

The existing `.gitignore` excludes generated scan/report artifact directories, but auditors are still responsible for checking `git status --short` before handoff.

## Evidence Quality Checks

For each finding, confirm:

- affected surface is clear
- user role is clear
- expected safe behavior is clear
- observed behavior is supported by evidence
- sensitive values are redacted
- reproduction or limitation is recorded
- confidence matches evidence quality
- severity matches business impact
- report language separates observation from inference
