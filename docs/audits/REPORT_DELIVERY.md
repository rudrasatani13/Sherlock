# Report Delivery Workflow

Status: Phase 8 Manual Audit Workflow

Report delivery defines how Sherlock prepares and delivers a manual AI launch security audit report without implementing report-generation code, PDF export, backend APIs, dashboards, or persistence.

The Phase 4 sample report in `docs/sample-report.md` and `apps/web/sample-report.html` remains a static reference. Phase 8 uses that structure manually; it does not create a report generator.

## Delivery Goals

- Communicate tested scope, observed behavior, impact, and fixes clearly.
- Avoid overclaiming.
- Provide redacted report evidence and practical remediation guidance.
- Make limitations and not-tested areas explicit.
- Define retest expectations.
- Ensure sensitive evidence is redacted before delivery.

## Report Preparation Workflow

1. Confirm final approved scope.
2. Confirm tested and not-tested categories.
3. Review all candidate findings.
4. Deduplicate findings.
5. Confirm severity and confidence.
6. Redact evidence.
7. Draft executive summary.
8. Draft launch readiness verdict.
9. Identify top 3 fixes.
10. Prepare findings table.
11. Prepare detailed findings.
12. Add tested scope, not-tested scope, assumptions, and limitations.
13. Add retest plan.
14. Review for overclaiming and sensitive data.
15. Deliver through the approved channel.
16. Hold or schedule client review.

## Recommended Report Structure

A final manual report should include:

1. Cover and metadata
2. Confidentiality or distribution label
3. Executive summary
4. Launch readiness verdict
5. Top 3 fixes
6. Findings table
7. Detailed findings
8. Evidence summaries
9. Reproduction summaries
10. Fix recommendations
11. Tested scope
12. Not-tested scope
13. Assumptions
14. Limitations
15. Retest plan
16. Final recommendation

## Executive Summary

The executive summary should explain:

- what Sherlock tested
- why the tested surfaces matter before launch
- most important risks observed
- which fixes should happen first
- whether high-impact findings need manual review or retest
- what was not tested
- why passing the audit does not guarantee complete security

## Launch Readiness Verdict

The launch readiness verdict should be scoped and evidence-based.

Examples:

- Launch-ready for the tested scope with no blocking findings observed.
- Launch-ready after Medium and Low remediation is scheduled.
- Not launch-ready until Critical and High findings are fixed and retested.
- Inconclusive because required access, logs, or scope were unavailable.

The verdict must explain limitations and should not imply the entire AI app is secure.

## Top 3 Fixes

Top fixes should prioritize:

- highest severity
- highest business impact
- broadest risk reduction
- launch blockers
- fixes that reduce multiple findings
- client engineering practicality

Each top fix should include an owner-friendly action statement and why it matters.

## Findings Table

Include:

- finding ID
- title
- category
- severity
- confidence
- status
- affected surface
- retest status if applicable

## Detailed Findings

Each detailed finding should include:

- title
- category
- severity
- confidence
- status
- affected surface
- tested role
- observed behavior
- expected behavior
- business impact
- evidence summary
- safe reproduction summary
- fix recommendation
- retest guidance
- assumptions and limitations

## Evidence Summaries

Evidence summaries should:

- use short redacted snippets
- explain what was observed
- avoid long transcripts
- avoid raw attack prompts unless explicitly approved
- avoid real customer data
- avoid secrets, tokens, keys, credentials, cookies, and private documents
- mark demo/canary values clearly

## Reproduction Summaries

Reproduction summaries should be safe and defensive.

Include:

- target surface
- test account role
- scenario ID or prompt-library ID when applicable
- high-level interaction summary
- expected safe behavior
- observed behavior
- reproduction count
- limitations

Do not include destructive exploit instructions or steps for attacking third-party systems.

## Tested Scope

Include:

- target systems
- environments
- test accounts or roles
- categories tested
- date and time of testing
- scanner/evaluator usage where applicable
- manual playbooks used
- rate limits or constraints

## Not-Tested Scope

Include:

- out-of-scope targets
- categories not tested
- unavailable accounts or roles
- unavailable logs or traces
- third-party systems not tested
- production paths not tested
- destructive actions not tested
- public self-serve scanning not enabled

## Limitations

Limitations may include:

- model nondeterminism
- missing retrieval traces
- missing tool logs
- missing source confirmation
- staging differs from production
- test accounts have limited permissions
- prompt-library execution was not integrated into public scanning
- evaluator is deterministic and pattern-based
- manual review was required for ambiguous results

## Required Language Boundaries

Reports must not say:

- "your AI app is secure"
- "100% protected"
- "certified safe"
- "all vulnerabilities found"
- "no risk exists"
- "Sherlock proves this system is safe"
- "no future attack can bypass this"

Reports may say:

- "Sherlock tested selected categories under the stated scope."
- "Passing this audit does not guarantee complete security."
- "Manual review is recommended for high-impact findings."
- "No issue was observed in the tested category under the documented scope."
- "This finding was reproduced under the documented test conditions."
- "The result is limited to the tested target, data, model behavior, and configuration at the time of testing."

## Delivery Process

Before delivery:

- Confirm client-approved delivery channel.
- Confirm distribution list.
- Confirm report version and date.
- Confirm all evidence is redacted and appropriate for report display.
- Confirm raw evidence is not attached unless explicitly approved.
- Confirm no overclaiming language exists.
- Confirm retest plan is included.

After delivery:

- Schedule or hold report walkthrough.
- Review Critical and High findings first.
- Confirm remediation owners if client wants to share them.
- Agree retest timing and scope.
- Record accepted risks or false positives if changed during discussion.
- Record follow-up questions and evidence requests.

## Final Recommendation

The final recommendation should be scoped.

Examples:

- Fix and retest Critical and High findings before broad launch.
- Proceed with launch only under documented risk acceptance and compensating controls.
- Retest retrieval and tool boundaries after remediation.
- Treat untested categories as remaining risk, not as passed checks.

Do not present a final recommendation as certification or complete-security assurance.
