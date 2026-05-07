# Client Intake Workflow

Status: Phase 8 Manual Audit Workflow

Client intake collects the minimum information needed to decide whether Sherlock can safely perform a manual or semi-automated AI security audit.

Completed intake records may contain sensitive business context. Store completed copies outside Git and share them only with authorized audit participants.

## Intake Goals

- Confirm the client, target app, and business owner.
- Understand the AI surface and launch context.
- Identify data, RAG, tool, and customer-data sensitivity.
- Capture testing windows, rate limits, and operational constraints.
- Confirm written authorization and out-of-scope targets.
- Determine whether the audit can proceed safely.

## Intake Sequence

1. Collect basic client and application details.
2. Identify the AI app type and target surfaces.
3. Ask data sensitivity and integration questions.
4. Capture test accounts, environment, windows, and rate limits.
5. Confirm authorization and out-of-scope systems.
6. Produce a draft audit scope for client approval.
7. Do not run tests until authorization and scope are approved.

## Required Intake Fields

### Client and Application

- Client or company name
- Legal entity name if different from operating name
- Primary contact name, role, and email
- Security or engineering escalation contact
- App name
- App URL
- API endpoint if applicable
- Environment: pre-launch, staging, production, or other
- Desired audit start and delivery dates

### AI App Type

Record all that apply:

- chatbot
- RAG or knowledge-base assistant
- agent
- tool-using app
- support bot
- internal assistant
- customer-data-connected AI app
- workflow copilot
- output-rendering surface such as web, email, document, ticket, or admin UI

### Target Type

Record each target surface separately:

- user-facing chat UI
- internal chat UI
- API endpoint
- retrieval or document Q&A endpoint
- agent workflow
- tool/function execution path
- admin or support workflow
- output rendering path
- staging or demo environment

### Data Sensitivity

Ask and record:

- Does the app process customer data?
- Does the app process personal data?
- Does the app process regulated, financial, health, support, billing, or compliance data?
- Does the app access private documents, internal notes, tickets, source content, or logs?
- Are any synthetic canary values available for testing?
- Are there data types that must never be included in evidence?
- Are there jurisdiction, contractual, or retention constraints?

### RAG and Private Documents

Ask and record:

- Are RAG or private documents involved?
- What document collections, tenants, roles, or permission boundaries exist?
- Are source citations exposed to users?
- Are retrieval traces available to the client for validation?
- Can the client provide synthetic documents or canaries for safe testing?
- Which document stores or collections are out of scope?

### Tools and Actions

Ask and record:

- Are tools, functions, workflows, or actions connected?
- Which tools are read-only?
- Which tools can modify data, send messages, spend money, change permissions, or affect customers?
- Are tools mocked, disabled, or isolated for testing?
- Are confirmation gates required before actions execute?
- Are tool logs available for review?
- Which actions are forbidden during testing?

### Test Accounts

Record:

- Test account identifiers or role names
- Test account roles and permissions
- Whether accounts are synthetic, staging, internal, or production-limited
- Credential handoff owner and secure delivery method
- MFA requirements
- Account reset process
- Account restrictions
- Whether lower-privileged and higher-privileged roles are available for permission tests

Do not paste passwords, API keys, session tokens, private keys, cookies, or one-time codes into the intake document.

### Testing Windows and Rate Limits

Record:

- Approved dates and times for testing
- Time zone
- Production blackout windows
- Maximum requests per minute or hour
- Maximum total requests or prompts
- Maximum model spend or usage budget if known
- Maximum concurrent sessions
- Expected system owners online during testing
- Pause or stop conditions

### Authorization and Scope

Record:

- Written authorization status
- Authorization signer and role
- Authorized tester names or team
- In-scope domains, URLs, APIs, apps, workspaces, tenants, accounts, and environments
- Out-of-scope domains, APIs, third-party services, tenants, accounts, and environments
- Forbidden actions
- Evidence handling requirements
- Retention or deletion expectations

## Intake Acceptance Criteria

Intake is complete only when:

- Client identity and primary contact are known.
- Target app and environment are clearly identified.
- AI app type and target surfaces are documented.
- Data sensitivity is understood.
- Customer-data, RAG, private-document, and tool/action use is documented.
- Test accounts are available or a plan exists to provision them.
- Testing windows and rate limits are defined.
- Written authorization is confirmed or explicitly pending.
- In-scope and out-of-scope targets are clear.
- A draft audit scope can be prepared.

## Stop Conditions

Pause intake or testing if:

- The requester cannot prove authorization.
- The target appears to belong to a third party not covered by written permission.
- Test accounts are unavailable or unsafe to use.
- The client asks for destructive production testing without an isolated, explicitly authorized environment.
- Data handling requirements are unclear for sensitive outputs.
- Rate limits, testing windows, or escalation contacts are missing for production targets.

## Template

Use `templates/audit-intake.md` for lightweight manual intake preparation. Completed client copies should be stored outside Git.
