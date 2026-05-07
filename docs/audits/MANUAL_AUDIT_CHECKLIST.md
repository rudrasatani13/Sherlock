# Manual Audit Checklist

Status: Phase 8 Manual Audit Workflow

Use this checklist to track a Sherlock manual or semi-automated audit from intake through closure.

Completed checklists may contain sensitive client details. Store completed copies outside Git.

## Intake and Authorization

- [ ] Intake complete
- [ ] Client/company name recorded
- [ ] App name and target surfaces recorded
- [ ] Data sensitivity reviewed
- [ ] Customer-data involvement reviewed
- [ ] RAG/private-document involvement reviewed
- [ ] Tool/action involvement reviewed
- [ ] Testing windows recorded
- [ ] Rate limits recorded
- [ ] Primary contact recorded
- [ ] Escalation contact recorded
- [ ] Authorization confirmed
- [ ] Authorization notes stored safely
- [ ] Out-of-scope targets recorded

## Scope Confirmation

- [ ] Target scope confirmed
- [ ] Environments confirmed
- [ ] Test accounts listed by role
- [ ] Forbidden actions listed
- [ ] Allowed categories selected
- [ ] Data handling rules confirmed
- [ ] Report expectations confirmed
- [ ] Scope approved by client

## Test Setup

- [ ] Test account ready
- [ ] Secure credential handoff completed outside Git
- [ ] Scanner config prepared
- [ ] Scanner config checked for secrets before use
- [ ] Prompt library selected
- [ ] Phase 6 prompt-library categories mapped to approved scope
- [ ] Synthetic canaries or demo fixtures prepared where applicable
- [ ] Rate limits and pauses configured operationally
- [ ] Evidence folders kept outside Git or ignored paths

## Scanner and Evaluator

- [ ] Scanner execution approved for the target and window
- [ ] Phase 5 scanner executed only against authorized target if applicable
- [ ] Scanner output stored under ignored/protected location
- [ ] Evaluator output reviewed
- [ ] Phase 7 matched signals reviewed
- [ ] Phase 7 redacted evidence reviewed
- [ ] `needs_manual_review` items queued for human review
- [ ] Scanner/evaluator limitations documented

## Manual Testing

- [ ] Manual tests completed
- [ ] Prompt injection playbook completed if in scope
- [ ] System prompt leakage playbook completed if in scope
- [ ] Sensitive data leakage playbook completed if in scope
- [ ] RAG data leakage playbook completed if in scope
- [ ] Indirect prompt injection playbook completed if in scope
- [ ] Tool/function abuse playbook completed if in scope
- [ ] Unsafe output handling playbook completed if in scope
- [ ] Cost abuse playbook completed if in scope
- [ ] Manual limitations documented

## Evidence Handling

- [ ] Evidence captured
- [ ] Evidence minimized to short snippets
- [ ] Evidence redacted
- [ ] Secrets, tokens, API keys, passwords, cookies, private keys, and one-time codes removed
- [ ] Real customer data excluded or redacted
- [ ] Demo/canary values clearly marked
- [ ] Raw evidence separated from report-safe evidence
- [ ] Evidence access restricted
- [ ] Evidence retention/deletion expectations recorded
- [ ] No evidence or scan outputs committed to Git

## Finding Review

- [ ] Findings deduplicated
- [ ] Automated verdicts reviewed
- [ ] Matched signals reviewed
- [ ] Category confirmed
- [ ] Severity/confidence reviewed
- [ ] False positives marked
- [ ] Needs-manual-review items resolved or documented
- [ ] Business impact written
- [ ] Fix recommendation written
- [ ] Retest steps defined

## Report Preparation and Delivery

- [ ] Report drafted
- [ ] Executive summary written
- [ ] Launch readiness verdict written
- [ ] Top 3 fixes identified
- [ ] Findings table prepared
- [ ] Detailed findings prepared
- [ ] Evidence summaries included safely
- [ ] Reproduction summaries included safely
- [ ] Tested scope included
- [ ] Not-tested scope included
- [ ] Limitations included
- [ ] Retest plan included
- [ ] Report reviewed
- [ ] Report checked for overclaiming
- [ ] Report delivered
- [ ] Client review meeting completed or scheduled

## Retest and Closure

- [ ] Retest planned
- [ ] Retest owner assigned
- [ ] Retest target and window confirmed
- [ ] Retest statuses recorded where applicable
- [ ] Audit closed
- [ ] Findings reviewed with client
- [ ] Evidence storage reviewed
- [ ] Sensitive data deletion/retention handled
- [ ] Internal notes updated
- [ ] Test accounts disabled or returned if applicable
- [ ] Test fixtures cleaned up if applicable
- [ ] Testimonial or case-study request considered if appropriate
