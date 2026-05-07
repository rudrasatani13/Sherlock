# Audit Closure Workflow

Status: Phase 8 Manual Audit Workflow

Audit closure confirms that the Sherlock manual audit engagement has been delivered, reviewed, retained or deleted according to expectations, and marked closed internally.

Completed closure records may contain client details and should be stored outside Git.

## Closure Goals

- Confirm final report delivery.
- Confirm findings were reviewed with the client.
- Confirm retest plan or risk acceptance.
- Review evidence storage and deletion expectations.
- Update internal notes.
- Close the audit cleanly without leaving sensitive artifacts unmanaged.

## Closure Checklist

- [ ] Report delivered
- [ ] Report delivery channel recorded
- [ ] Report version recorded
- [ ] Findings reviewed with client
- [ ] Critical and High findings discussed first
- [ ] Retest plan agreed or explicitly deferred
- [ ] Accepted risks recorded where applicable
- [ ] False positives recorded where applicable
- [ ] Evidence storage reviewed
- [ ] Sensitive data deletion/retention handled
- [ ] Raw evidence access reviewed
- [ ] Report-safe evidence archived according to agreement
- [ ] Scanner outputs reviewed and deleted or retained according to agreement
- [ ] Evaluator outputs reviewed and deleted or retained according to agreement
- [ ] Test accounts disabled, returned, or confirmed inactive if applicable
- [ ] Synthetic test fixtures cleaned up if applicable
- [ ] Internal notes updated
- [ ] Follow-up owner assigned if applicable
- [ ] Testimonial or case-study request considered if appropriate
- [ ] Audit marked closed

## Closure Workflow

1. Confirm report delivery.
2. Confirm client received and can access the report.
3. Hold or schedule findings review.
4. Record client questions, accepted risks, and false-positive decisions.
5. Agree retest plan, retest scope, and timing.
6. Review raw and report-safe evidence storage.
7. Delete or retain evidence according to the agreed retention plan.
8. Confirm generated scan and evaluator outputs are not committed to Git.
9. Update internal audit notes.
10. Close test accounts and synthetic fixtures if applicable.
11. Consider testimonial or case-study request if appropriate.
12. Mark audit closed.

## Evidence Retention Review

At closure, confirm:

- raw evidence location
- report-safe evidence location
- scan output location
- evaluator output location
- authorization notes location
- access list
- retention deadline
- deletion owner
- deletion confirmation requirement

If the client requires deletion, record what was deleted and when.

## Retest Plan Review

Record:

- findings selected for retest
- categories selected for retest
- expected remediation date
- retest window
- retest owner
- required accounts or logs
- whether scanner/evaluator can be rerun
- whether manual validation is required

If no retest is planned, record why.

## Accepted Risk Review

Accepted risk should include:

- finding ID
- risk owner
- acceptance reason
- compensating controls if any
- date accepted
- review date if applicable

Do not mark a finding fixed if the client accepts the risk without remediation and retest.

## Case Study or Testimonial

Only request a testimonial or case-study discussion when appropriate.

Do not use:

- client name
- logo
- target details
- finding details
- evidence
- screenshots
- metrics
- quotes

unless the client explicitly approves the use and wording.

## Closure Notes

Closure notes should summarize:

- audit name
- client
- report version delivered
- date delivered
- reviewed findings
- agreed retest plan
- evidence retention/deletion decision
- remaining limitations
- next steps
- closure date

## Template

Use `templates/audit-closure.md` for lightweight closure tracking. Completed client closure records should be stored outside Git.
