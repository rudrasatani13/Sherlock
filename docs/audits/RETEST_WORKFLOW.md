# Retest Workflow

Status: Phase 8 Manual Audit Workflow

Retesting verifies whether client remediation changed the observed behavior under the original test conditions or an approved equivalent.

Retesting does not prove complete security. It records whether the specific finding, category, or scenario appears fixed, still vulnerable, partially fixed, inconclusive, accepted risk, or still needs manual review.

## Retest Goals

- Validate fixes for selected findings or categories.
- Confirm high-impact findings with manual validation.
- Reuse original test conditions where possible.
- Record remaining limitations.
- Update finding status accurately.
- Avoid overclaiming after a passed retest.

## Retest Triggers

Retest may occur when:

- client says a finding is fixed
- client changes prompts, retrieval, tools, permissions, output rendering, or limits
- client changes model, provider, agent framework, or RAG pipeline
- client requests validation before launch
- a high-impact finding requires confirmation before delivery
- an accepted-risk decision changes

## Retest Inputs

Collect:

- original finding ID
- original category
- original affected surface
- original tested role
- original scenario or prompt-library ID
- original expected safe behavior
- original evidence summary
- remediation summary from client
- new testing window
- approved retest scope
- rate limits and forbidden actions

## Retest Process

1. Client fixes or changes the issue.
2. Auditor selects the finding or category for retest.
3. Auditor confirms authorization and retest window.
4. Auditor reviews the original evidence and retest steps.
5. Scanner/evaluator can be rerun where applicable.
6. Manual validation is performed for high-impact findings.
7. Evidence is captured and redacted.
8. Retest result is recorded.
9. Report or closure notes are updated.

## Scanner and Evaluator Use

Where applicable:

- Re-run the Phase 5 scanner only against authorized targets.
- Keep outputs under ignored/protected `scan-results/` locations.
- Run the Phase 7 evaluator against new scanner output if relevant.
- Compare evaluator verdicts, matched signals, redacted evidence, severity, confidence, and manual-review flags.
- Treat evaluator changes as review inputs, not final proof.

Manual validation is required for high-impact findings, ambiguous sensitive-data cases, tool/action questions, and customer-facing report updates.

## Retest Statuses

### Fixed

Use when the original issue no longer reproduces under the documented conditions and evidence supports closure.

### Still Vulnerable

Use when the original issue still reproduces or equivalent unsafe behavior remains.

### Partially Fixed

Use when remediation reduced risk but did not fully resolve the issue.

Examples:

- one role is fixed but another remains affected
- direct prompt path is fixed but indirect path remains
- data is redacted but unauthorized document metadata still appears
- tool execution is blocked but unsafe preparation still occurs

### Inconclusive

Use when retest evidence is insufficient.

Examples:

- target unavailable
- logs unavailable
- model behavior inconsistent
- account permissions changed in a way that prevents comparison
- retest scope differs materially from original scope

### Accepted Risk

Use when the client acknowledges the remaining issue and accepts it.

Record:

- risk owner
- reason
- date
- compensating controls if any
- planned follow-up if any

### Needs Manual Review

Use when retest evidence suggests a possible issue but sensitivity, permissions, exploitability, or business impact needs confirmation.

## High-Impact Retest Rules

For Critical and High findings:

- Validate manually even if automated signals no longer appear.
- Confirm the control is enforced outside the model when relevant.
- Confirm no equivalent bypass path remains in the tested scope.
- Review logs, retrieval traces, or tool traces when available.
- Document limitations if exact reproduction conditions changed.

## Evidence for Retest

Collect:

- retest date and tester
- target and environment
- tested role
- remediation summary
- retest scenario or test ID
- expected fixed behavior
- observed behavior
- scanner/evaluator output reference if applicable
- manual evidence summary
- redaction notes
- final retest status

## Retest Report Language

Use scoped language:

- "The original scenario did not reproduce during retest under the documented conditions."
- "The finding is marked Fixed for the tested scope."
- "This retest does not guarantee that all variants are fixed."
- "Manual review remains recommended for high-impact or ambiguous behavior."

Avoid:

- "the vulnerability is impossible now"
- "the app is secure"
- "all related issues are fixed"
- "no risk remains"

## Retest Closure Criteria

A retest record is complete when:

- original finding is identified
- retest scope is approved
- retest method is documented
- evidence is redacted
- status is assigned
- limitations are recorded
- client is informed of the result
- report or closure notes are updated

## Template

Use `templates/retest-record.md` for lightweight retest documentation. Completed client retest records should be stored outside Git.
