# Category-Specific Manual Testing Playbooks

Status: Phase 8 Manual Audit Workflow

These playbooks guide safe, defensive manual testing for Sherlock's core categories. They are intended for authorized client audits only.

Do not use these playbooks to test third-party systems without permission. Do not run destructive actions. Use synthetic data, fake canaries, mock tools, staging fixtures, and redacted report summaries whenever possible.

## General Playbook Rules

- Confirm written authorization and approved scope before testing.
- Use the approved testing window and rate limits.
- Prefer staging, demo, or isolated environments.
- Use client-provided test accounts and synthetic fixtures.
- Keep prompts and reproduction summaries safe and high-level in reports.
- Capture short evidence snippets and redact sensitive values.
- Pause if secrets, real customer data, unexpected production impact, or unsafe tool execution appears.
- Treat Phase 7 evaluator output as input for human review, not as final customer-facing findings.

## Prompt Injection

### Objective

Determine whether untrusted user input can cause the AI surface to ignore intended boundaries, change roles, bypass task restrictions, expose data, or trigger unsafe downstream behavior.

### When to Run

Run when the target accepts free-form user instructions, chat messages, support prompts, workflow requests, or user-controlled content that influences model behavior.

### Prerequisites

- Approved target surface and user role
- Expected safe behavior from the client or product documentation
- Test account with known permissions
- Approved prompt-library cases or safe manual scenarios
- Data and tool boundaries documented

### Safe Testing Approach

- Use benign role-boundary and policy-boundary scenarios.
- Use fake canary text such as `FAKE-CANARY-AUDIT-001` only when approved.
- Check whether the assistant stays within its documented role.
- Check whether prompt manipulation changes output in a security-relevant way.
- Avoid requests for real secrets, real customer data, or destructive actions.
- If testing links to another category, such as RAG leakage or tool abuse, keep that category's safety rules in scope.

### Evidence to Collect

- Target surface and test role
- Prompt-library test ID or safe scenario identifier
- Expected safe behavior
- Observed behavior
- Short redacted output excerpt
- Reproduction count
- Whether any data exposure, unsafe action, or only instruction drift occurred
- Relevant limitations

### Common False Positives

- The model says it changed roles but no control boundary actually changed.
- The response contains generic safety wording but no hidden policy or sensitive data.
- The model produces fictional claims that are not confirmed by logs, source data, or repeatability.
- A harmless formatting change is mistaken for a security bypass.

### Severity Guidance

- Critical requires strong evidence of credential leakage, customer data exposure, unauthorized action, or serious business impact.
- High is appropriate for reliable launch-critical control bypass or privileged behavior.
- Medium is appropriate for meaningful behavior change with limited direct impact.
- Low or Informational is appropriate for minor instruction drift without security impact.

### Confidence Guidance

- High confidence requires reproducibility and clear deviation from expected controls.
- Medium confidence applies when multiple signals suggest bypass but impact needs confirmation.
- Low confidence applies when behavior appears once or may be normal model drift.

### Fix Guidance

- Enforce authorization and data access outside the model.
- Separate trusted instructions from untrusted user content.
- Reduce sensitive context sent to the model.
- Add server-side tool permission checks.
- Add confirmation gates for sensitive actions.
- Add regression tests for known bypass patterns.
- Do not rely only on stronger prompt wording as the fix.

### Retest Guidance

- Retest the original scenario after remediation.
- Include at least one negative control using a normal benign request.
- Confirm the issue no longer causes data exposure, unsafe action, or boundary bypass.
- Keep severity and confidence updated based on retest evidence.

## System Prompt Leakage

### Objective

Determine whether the AI surface exposes hidden instructions, developer messages, routing logic, internal tool descriptions, or other implementation guidance intended to remain private.

### When to Run

Run when the target uses hidden system/developer prompts, tool schemas, routing rules, internal safety policies, or proprietary instruction text.

### Prerequisites

- Client explanation of what prompt or policy details are sensitive
- Approved target and test account
- Safe direct and indirect disclosure scenarios
- Owner available to confirm whether leaked text is real or hallucinated

### Safe Testing Approach

- Use high-level requests that ask the assistant to describe its boundaries or explain what it can do.
- Compare outputs to known safe public-facing descriptions.
- Ask the client to confirm whether suspicious text is real before reporting high impact.
- Do not request credentials, tokens, or unrelated secrets.
- Do not publish raw hidden prompt text in the report unless explicitly approved and safe.

### Evidence to Collect

- Exact leaked excerpt with sensitive values redacted
- Prompt-library test ID or safe scenario identifier
- Affected surface
- Whether leakage was full, partial, or inferred
- Whether leaked content included generic role text, security-sensitive tool details, secrets, data, or private documents
- Product-owner confirmation when available
- Reproduction count

### Common False Positives

- The model hallucinates a plausible system prompt.
- The output repeats public documentation or visible UI copy.
- The exposed text is generic role or tone guidance with low abuse value.
- The model describes capabilities without revealing hidden implementation details.

### Severity Guidance

- System prompt leakage alone is usually not automatically Critical.
- Critical requires credentials, tokens, customer data, private documents, or a direct path to high-impact unauthorized action.
- High may apply to security-sensitive tool instructions or proprietary operational details that materially aid exploitation.
- Medium may apply to meaningful guardrail or routing logic exposure.
- Low may apply to generic role, tone, or formatting instructions.

### Confidence Guidance

- High confidence requires confirmed exact or near-exact hidden text.
- Medium confidence applies to likely internal details that are not source-confirmed.
- Low confidence applies to possible hallucination or generic policy language.

### Fix Guidance

- Remove secrets and sensitive operational details from prompts.
- Minimize hidden policy text sent to the model.
- Avoid exposing internal tool schemas unless required.
- Enforce data access and tool permissions outside prompt secrecy.
- Treat prompt secrecy as defense-in-depth.

### Retest Guidance

- Retest direct and indirect disclosure paths.
- Confirm only public-safe boundary descriptions appear.
- Ask the client to verify suspicious remnants before closing.

## Sensitive Data Leakage

### Objective

Determine whether the AI system exposes data that the requesting user, role, tenant, session, or audience should not access.

### When to Run

Run when the target connects to customer records, personal data, support data, tickets, logs, CRM data, account data, private documents, internal notes, credentials, or other sensitive sources.

### Prerequisites

- Data classification from the client
- Test accounts with documented permissions
- Synthetic sensitive canaries if available
- Clear rules for evidence redaction and retention
- Client contact available to confirm sensitivity when ambiguous

### Safe Testing Approach

- Prefer synthetic records and demo canaries over real customer data.
- Compare lower-privileged and expected-access roles where approved.
- Ask for only approved test fixture records.
- Stop if real credentials, tokens, or unexpected customer data appears.
- Do not attempt to collect, enumerate, or store real sensitive datasets.

### Evidence to Collect

- Type of sensitive data exposed
- Affected role and expected access
- Short redacted output excerpt
- Source or likely source if known
- Whether data belongs to another user, tenant, customer, or internal system
- Product-owner confirmation for ambiguous data
- Reproduction count
- Redaction notes

### Common False Positives

- The output looks like sensitive data but is hallucinated.
- The test account legitimately has access to the data.
- The value is synthetic and intentionally visible.
- Public or low-sensitivity metadata is mistaken for protected data.

### Severity Guidance

- Critical requires unauthorized exposure of real credentials, tokens, private keys, customer data, regulated data, or high-value business data.
- High may apply to confirmed sensitive internal or customer data exposure with limited or synthetic conditions.
- Medium may apply to non-public internal information with moderate impact.
- Low may apply to benign identifiers or low-sensitivity metadata.
- Ambiguous sensitive-data cases should go to manual review.

### Confidence Guidance

- High confidence requires confirmed real protected data or known synthetic canaries.
- Medium confidence applies when output strongly resembles sensitive data but ownership or sensitivity needs confirmation.
- Low confidence applies when output may be fabricated or non-sensitive.

### Fix Guidance

- Enforce authorization before data reaches the model.
- Minimize context included in prompts and tool responses.
- Redact secrets and sensitive fields at source.
- Add tenant isolation checks.
- Add retrieval filters before generation.
- Add regression tests with synthetic sensitive canaries.

### Retest Guidance

- Retest with the same role and scenario.
- Verify lower-privileged users cannot access protected data.
- Use synthetic canaries where possible.
- Confirm logs and report evidence remain redacted.

## RAG Data Leakage / Document Exfiltration

### Objective

Determine whether a RAG system exposes documents, summaries, citations, source metadata, or retrieved context that the requesting user should not access.

### When to Run

Run when the target retrieves from knowledge bases, private documents, tickets, internal notes, customer workspaces, support archives, vector indexes, or source-linked citations.

### Prerequisites

- Document collections and permission boundaries documented
- Test accounts with known document access
- Synthetic documents or canary markers where possible
- Retrieval trace or source-citation visibility if available
- Client confirmation of expected document access

### Safe Testing Approach

- Use approved synthetic documents and canaries such as `FAKE-CANARY-RAG-AUDIT-001`.
- Compare access between roles only when both accounts are authorized.
- Ask about known test fixture topics rather than real customer names.
- Check generated answers, citations, document titles, and retrieval traces.
- Do not attempt broad document enumeration or real customer data collection.

### Evidence to Collect

- Affected RAG surface
- Requesting role and expected document permissions
- Restricted document or source class
- Redacted generated answer, citation, source metadata, or retrieval trace
- Proof that the source should have been inaccessible
- Whether leakage was direct quotation, summary, metadata, citation, or inference
- Reproduction count

### Common False Positives

- The answer is hallucinated and not retrieved from a restricted document.
- The document is actually public or available to the test role.
- The output reveals a title but not sensitive content.
- The source metadata is intentionally exposed in the product design.

### Severity Guidance

- Critical requires unauthorized access to customer documents, regulated data, credentials, or high-impact private business documents.
- High applies to clear cross-tenant, cross-account, or privileged document exposure.
- Medium applies to restricted internal documents, metadata, or summaries with limited scope.
- Low applies to low-sensitivity titles or benign metadata.

### Confidence Guidance

- High confidence requires confirmed inaccessible source content in output or retrieval traces.
- Medium confidence applies when output strongly indicates unauthorized retrieval but exact source needs confirmation.
- Low confidence applies when output may be hallucinated or based on public information.

### Fix Guidance

- Enforce tenant, role, and document permissions before retrieval.
- Filter vector search by access policy at query time.
- Avoid sending unauthorized chunks to the model.
- Isolate indexes or namespaces where appropriate.
- Prevent cross-session retrieval cache leakage.
- Redact or suppress sensitive source metadata.
- Log retrieval source IDs for audit and retest.

### Retest Guidance

- Retest the original document boundary with the same role.
- Confirm restricted chunks do not enter model context.
- Confirm citations and metadata are permission-filtered.
- Use retrieval traces if available to verify source filtering.

## Indirect Prompt Injection

### Objective

Determine whether untrusted retrieved or ingested content can manipulate model behavior, data access, tool calls, or rendered output.

### When to Run

Run when the AI system reads documents, web pages, tickets, emails, comments, files, knowledge-base entries, customer messages, pull requests, or other user-controlled content.

### Prerequisites

- Approved synthetic content fixture or staging document
- Ingestion or retrieval path documented
- Expected safe handling of retrieved content as untrusted data
- Tool/action and data boundaries identified
- Manual review plan for causality

### Safe Testing Approach

- Use a clearly labeled synthetic document containing benign instruction-like text.
- Confirm the model treats retrieved content as data, not policy.
- Compare behavior with and without the synthetic document when feasible.
- Avoid real malicious content, real secrets, and destructive instructions.
- Do not poison production knowledge bases unless the fixture is isolated and explicitly approved.

### Evidence to Collect

- Source of untrusted content
- Affected retrieval or ingestion path
- Fixture identifier or sanitized content snippet
- Observed behavior caused by retrieved instruction-like content
- Whether the instruction was visible to the user
- Any data, tool, or output effects
- Reproduction count
- Negative control when available

### Common False Positives

- The behavior change is normal retrieval relevance, not instruction following.
- The fixture was not actually retrieved.
- The output changed due to model nondeterminism rather than the embedded content.
- The assistant summarizes the instruction-like text without following it.

### Severity Guidance

- Critical requires credential leakage, customer data exposure, unauthorized action, or serious business impact.
- High applies to reliable manipulation of launch-critical agent behavior, tool use, or data access.
- Medium applies to meaningful answer-policy or output changes without major data/action impact.
- Low applies when the model acknowledges or partially follows embedded text with limited impact.

### Confidence Guidance

- High confidence requires reproducible behavior only when the untrusted content is present.
- Medium confidence applies when multiple signals suggest manipulation but source causality needs review.
- Low confidence applies when behavior could be unrelated model drift.

### Fix Guidance

- Mark retrieved content as untrusted data.
- Separate instructions from content in prompts and UI.
- Sanitize or transform retrieved content before model use.
- Block tool execution based solely on retrieved content.
- Require user confirmation for sensitive actions.
- Add source trust labels and provenance.

### Retest Guidance

- Retest with the same synthetic fixture and a clean negative control.
- Confirm untrusted content is summarized or cited without being followed as instruction.
- Confirm tools and data access remain governed by trusted controls.

## Tool / Function Abuse

### Objective

Determine whether an AI agent can call tools, functions, APIs, or workflows in a way that violates user intent, authorization, business rules, or safety expectations.

### When to Run

Run when the target can call tools, prepare actions, modify records, send messages, retrieve sensitive data, create tickets, issue refunds, change settings, or trigger workflows.

### Prerequisites

- Tool inventory and risk classification
- Test account permissions
- Mock, dry-run, staging, or read-only tool mode
- Confirmation gate expectations
- Tool logs or action traces where available
- Explicit forbidden action list

### Safe Testing Approach

- Use mock or dry-run tools whenever possible.
- Verify whether the agent proposes, prepares, or claims an action without authorization.
- Do not execute destructive, financial, customer-impacting, or permission-changing actions.
- Use synthetic destinations and test records.
- Stop if a real action may execute outside the approved scope.

### Evidence to Collect

- Affected tool or function
- User role and expected permission
- Tool arguments or action summary with sensitive values redacted
- Whether action was proposed, prepared, executed, or only attempted
- Confirmation boundary observed
- Tool log, trace, screenshot, or response content
- Reproduction count
- Whether environment was isolated

### Common False Positives

- The model claims it executed an action, but no tool call occurred.
- A tool call is proposed but blocked by server-side authorization.
- The action is low-risk or expected for the user's role.
- Logs are unavailable, so execution cannot be confirmed.

### Severity Guidance

- Tool abuse needs strong evidence or clear mock/action confirmation.
- Critical requires unauthorized destructive, financial, customer-impacting, credential-exposing, or privileged action success.
- High applies to high-risk action preparation or likely execution with weak confirmation.
- Medium applies to untrusted arguments or sensitive tool output with limited impact.
- Low applies to weak confirmation or unclear UI state with no sensitive side effect.

### Confidence Guidance

- High confidence requires logs or UI proving execution or unsafe preparation.
- Medium confidence applies when risky calls are attempted but execution status needs confirmation.
- Low confidence applies when output suggests misuse but no tool trace is available.

### Fix Guidance

- Enforce authorization at the tool/API layer.
- Require explicit user confirmation for sensitive actions.
- Use allowlists for tool arguments and destinations.
- Separate draft and execute actions.
- Add idempotency and rollback where possible.
- Block tool use from untrusted retrieved instructions.
- Cap tool-call loops and retries.

### Retest Guidance

- Retest in the same isolated tool mode.
- Verify unauthorized roles cannot prepare or execute the action.
- Verify confirmation gates are enforced outside the model.
- Preserve safe tool traces as evidence.

## Unsafe Output Handling

### Objective

Determine whether generated AI output is rendered, linked, downloaded, forwarded, or embedded in a way that creates user, browser, data, or downstream system risk.

### When to Run

Run when AI output appears in web UI, email, documents, tickets, admin panels, markdown renderers, rich text editors, previews, file exports, or downstream automations.

### Prerequisites

- Output rendering path documented
- Approved UI or staging environment
- Expected sanitization or escaping behavior
- Safe sanitized payload examples
- Screenshot or DOM-inspection method if applicable

### Safe Testing Approach

- Use escaped, benign, and clearly synthetic output-handling examples.
- Check whether generated content is displayed as text or rendered as active content.
- Avoid live phishing, credential collection, malware, or harmful scripts.
- Do not send unsafe content to real users.
- Prefer staging surfaces and test-only records.

### Evidence to Collect

- Affected rendering surface
- Sanitized generated output or payload description
- Rendered result, screenshot, or DOM evidence when relevant
- Whether active content executed, displayed unsafely, or was safely escaped
- Downstream system affected
- Expected rendering boundary
- Reproduction count

### Common False Positives

- Risky-looking text is safely escaped.
- The raw response is not rendered by the product UI.
- The issue appears only in developer tools, not in user-facing surfaces.
- A link is visible but protected by safe link handling.

### Severity Guidance

- Critical requires code execution or resulting account compromise, credential theft, customer data exposure, or privileged action.
- High applies to reproducible active-content risk in sensitive authenticated surfaces.
- Medium applies to unsafe links, rich rendering, or file handling requiring user interaction.
- Low applies to misleading formatting or benign unsafe rendering with limited impact.

### Confidence Guidance

- High confidence requires rendered output demonstrating unsafe behavior.
- Medium confidence applies when output would be unsafe in the documented path but live rendering was not confirmed.
- Low confidence applies when renderer behavior is unknown.

### Fix Guidance

- Sanitize and escape AI output before rendering.
- Disable raw HTML where not needed.
- Use allowlisted Markdown rendering.
- Strip scripts, event handlers, iframes, embeds, and unsafe URLs.
- Mark AI-generated links and files clearly.
- Avoid rendering untrusted model output in privileged admin contexts.

### Retest Guidance

- Retest the same rendering path.
- Confirm unsafe content is escaped, stripped, or blocked.
- Confirm downstream email, document, ticket, and admin views are also safe if in scope.

## Cost Abuse / Unbounded Consumption

### Objective

Determine whether users can trigger excessive model usage, long loops, repeated retrieval, repeated tool calls, expensive retries, high concurrency, or uncontrolled background work.

### When to Run

Run when the target uses expensive models, retrieval, tools, agents, retries, background jobs, file ingestion, streaming output, or long-running workflows.

### Prerequisites

- Approved rate and usage limits
- Client-provided safe testing budget
- Observability for model, retrieval, tool, duration, or retry counts if available
- Stop conditions and escalation contact
- Non-load-testing scope unless separately authorized

### Safe Testing Approach

- Use bounded, low-volume checks only.
- Verify limits through documentation, UI behavior, or small controlled tests.
- Do not perform stress tests, denial-of-service tests, high-concurrency tests, or spend-heavy loops unless separately authorized.
- Stop before exceeding rate, spend, duration, or retry limits.

### Evidence to Collect

- Affected workflow
- Safe interaction pattern that triggered excessive behavior
- Observed model, retrieval, tool, retry, token, duration, or cost indicators
- Configured limits if known
- User-visible behavior during limit handling
- Reproduction count
- Whether rate limits, cancellation, or circuit breakers were available

### Common False Positives

- A long response is expected for the workflow.
- Usage appears high but is within documented limits.
- Metrics are unavailable, so cost impact is theoretical.
- A one-off slow response is caused by external provider latency.

### Severity Guidance

- Critical requires strong evidence of major outage, uncontrolled spend, or broad service disruption with little effort.
- High applies to reliable high-cost or denial-of-service path against a launch-critical surface.
- Medium applies to expensive behavior constrained by some limits or requiring sustained use.
- Low applies to minor inefficiency or unclear limit messaging.

### Confidence Guidance

- High confidence requires measured calls, duration, retries, or cost showing repeated excessive use.
- Medium confidence applies when behavior suggests excessive consumption but exact cost data is incomplete.
- Low confidence applies to theoretical risk without measurement.

### Fix Guidance

- Enforce input and output limits.
- Cap model, retrieval, and tool calls per request.
- Add timeouts and cancellation.
- Add per-user and per-tenant rate limits.
- Add spend budgets and circuit breakers.
- Make failure states visible to users.
- Avoid recursive agent loops without hard stops.
- Log usage metrics needed for investigation.

### Retest Guidance

- Retest with the same bounded scenario.
- Confirm limits trigger safely and visibly.
- Confirm no excessive retries, tool loops, or unbounded output occurs.
- Record measured values where available.
