# Security Notes

Sherlock will eventually test AI systems that may connect to customer data, tools, internal APIs, and sensitive workflows. Security controls must be designed before real scanning is exposed to customers.

## Secrets

- Do not store API keys, provider tokens, database credentials, webhook secrets, or private keys in plain text.
- Do not commit `.env.local`, `.env.production`, or any real environment file.
- Use `.env.example` for placeholder values only.
- Prefer managed secret storage in deployed environments.

## Target Authorization

- Require ownership verification before scanning any URL, API, chatbot, RAG app, agent, or customer system.
- Keep verification state auditable.
- Do not run external scans against unverified targets.
- The Phase 5 internal scanner must only be used against targets the operator owns or is explicitly authorized to test.
- Phase 8 manual audits require written authorization, approved scope, testing windows, rate limits, escalation contacts, and documented out-of-scope targets before testing.

## Network Safety

- Prevent SSRF before adding URL or API scanning.
- Block private, internal, link-local, loopback, and metadata service IP ranges before allowing scan requests.
- Resolve and validate redirects, DNS rebinding behavior, and user-supplied hostnames.
- Add explicit timeouts, body limits, retry limits, and concurrency limits.

## Data Handling

- Scan logs may contain sensitive data.
- Store only what is necessary for evidence and debugging.
- Redact sensitive evidence in reports.
- Avoid retaining raw prompts, responses, headers, tokens, cookies, and uploaded files unless there is a clear reason and customer consent.
- Generated scan outputs and reports should not be committed.
- Phase 5 local scan outputs may contain sensitive target responses and should stay in ignored, protected folders such as `scan-results/`.
- Phase 8 audit evidence, completed client templates, authorization notes, report drafts, screenshots, and retest records may contain sensitive data and should stay outside Git.

## Reporting Language

- Reports must not claim "your AI app is secure."
- Passing a scan does not guarantee complete security.
- Findings should describe observed behavior, evidence, impact, limitations, and recommended remediation.
- Reports should use plain English, include tested scope, and avoid fearmongering or overclaiming.
- Reports should not claim "100% protected", "certified safe", "all vulnerabilities found", or "no risk exists."

## Severity and Confidence

- Use the severity and confidence systems in `docs/methodology.md`.
- Do not mark a finding Critical unless there is strong evidence of serious impact such as customer data exposure, unauthorized action, credential leakage, or major business risk.
- Low-confidence observations should be marked for manual review or treated as inconclusive unless impact is independently confirmed.
- System prompt leakage is not automatically critical. Severity depends on what leaked and what impact the leakage enables.

## Cost and Abuse Controls

- Add spend limits before automated scanner execution.
- Add rate limits before public scan creation.
- Add cancellation and timeout support before long-running scans.
- Do not allow unbounded prompt loops, tool calls, or retries.

## Tool and Function Abuse

Future tool-using-agent tests must avoid invoking destructive or high-risk actions unless the test target is isolated and explicitly authorized. Scanner design should make side effects visible and controllable.

## Manual Audit Workflow

- Use `docs/audits/README.md` as the Phase 8 manual audit workflow reference.
- Do not begin manual or semi-automated testing until intake, authorization, scope, data handling, and pause conditions are documented.
- Use safe defensive playbooks only.
- Do not test unauthorized third-party systems.
- Do not commit raw evidence, generated scan outputs, evaluator outputs, completed client templates, authorization records, or report drafts containing client data.
