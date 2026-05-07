# Authorization and Permission Rules

Status: Phase 8 Manual Audit Workflow

Sherlock audits must be authorized before any scanner execution or manual testing occurs.

## Core Rules

- Test only systems the client owns or is explicitly authorized to test.
- Require written authorization before testing.
- Define in-scope targets before testing.
- Define out-of-scope targets before testing.
- Do not test third-party systems without written permission from the appropriate owner.
- Avoid destructive actions.
- Avoid production impact.
- Respect rate limits, testing windows, and operational constraints.
- Pause testing if unexpected impact occurs.
- Store authorization notes safely and outside Git when they contain client details.

## Written Authorization Requirements

Written authorization should identify:

- Client legal entity or authorized business owner
- Authorization signer and role
- Authorized auditor or audit team
- Target app and target systems
- Environments covered by authorization
- Testing window
- Allowed categories and techniques
- Forbidden actions
- Rate limits and usage limits
- Data handling requirements
- Escalation contacts
- Authorization start date and expiration date

Email, signed statement of work, security testing addendum, or equivalent written approval is acceptable if it clearly covers the test scope.

## In-Scope Target Rules

In-scope targets must be specific enough to avoid accidental testing of unrelated systems.

Examples of acceptable in-scope definitions:

- `https://staging.example-client.test/ai-support`
- `POST https://api.staging.example-client.test/chat`
- Staging tenant `demo-tenant-a`
- Test accounts `support-viewer-demo` and `support-admin-demo`
- Synthetic document collection `demo-support-kb`
- Mock tool workflow `create_demo_ticket`

Avoid vague scope such as:

- all company systems
- any app owned by the client
- production AI features without a defined path
- third-party AI provider infrastructure
- customer tenants not explicitly approved for testing

## Out-of-Scope Target Rules

Out-of-scope targets should be documented explicitly.

Common out-of-scope items:

- Third-party provider systems
- Other client products not listed in scope
- Real customer tenants or accounts
- Production admin panels unless specifically approved
- Payment, billing, refund, deletion, email-sending, permission-changing, or destructive tool actions
- Internal infrastructure not required for AI audit testing
- Employee accounts not provisioned for testing
- Personal devices, browsers, or networks

## Third-Party Systems

Do not test third-party systems unless the client provides written authorization from the third-party owner or a contractual right that clearly allows the testing.

Examples requiring separate permission:

- Hosted chat vendors outside the client's control
- External SaaS products connected as tools
- Payment processors
- CRM systems
- Email providers
- Cloud provider control planes
- Public websites not owned by the client

If a target redirects, calls, retrieves from, or renders third-party services, keep testing limited to the authorized client surface and avoid probing the third-party system directly.

## Production Safety Rules

Production testing requires extra caution.

Before production testing:

- Confirm production is explicitly authorized.
- Confirm the testing window.
- Confirm rate limits and spend limits.
- Confirm escalation contacts are available.
- Confirm test accounts cannot access real customer data unless specifically authorized.
- Confirm tools are read-only, mocked, disabled, or safely constrained.
- Confirm evidence handling for any sensitive output.

Pause immediately if production impact is observed or suspected.

## Destructive Action Rules

Do not perform destructive actions during Phase 8 audits.

Forbidden unless isolated and explicitly authorized in writing:

- deleting records
- sending real emails or messages
- issuing refunds or payments
- changing permissions
- modifying customer data
- exporting real customer data
- triggering production workflows
- changing billing, subscription, access, or account state
- creating high-volume load or spend

Tool/function abuse testing should use mock actions, dry-run modes, read-only paths, or client-confirmed non-destructive staging fixtures.

## Rate Limit and Usage Rules

Respect client-provided limits.

Record:

- maximum prompts or requests
- maximum requests per minute or hour
- maximum concurrency
- model or API spend budget
- maximum test duration
- retry limits
- cancellation or pause procedure

If limits are not provided for a production target, do not start testing until safe defaults are approved.

## Pause Conditions

Pause testing and contact the escalation owner if:

- unexpected errors or outages occur
- response latency or resource use spikes unexpectedly
- production data appears in output unexpectedly
- credentials, tokens, or secrets appear in output
- a tool action executes or appears likely to execute outside the approved scope
- rate limits or spend limits may be exceeded
- scope ambiguity appears during testing
- the client revokes or modifies authorization

## Authorization Records

Keep authorization records accessible to the audit team but protected.

Authorization records should include:

- final approved scope
- written authorization evidence or reference
- date and time received
- approving person and role
- authorized tester list
- scope changes
- testing pause or resume notes
- closure confirmation

Do not commit client authorization records, signed documents, emails, or sensitive notes to Git.
