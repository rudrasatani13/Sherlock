# Sample Report Reference

Status: Phase 4 completed. Phase 8 manual report delivery workflow references this structure.

This document is the internal reference for the static PowerDetect Sherlock sample report.
It supports the public page at `apps/web/sample-report.html`.

The sample report is a sales, demo, and trust-building artifact only. It is not generated from a
real scan, not connected to a scanner engine, and not a customer report.

## Scope

The Phase 4 sample report demonstrates:

- report cover and metadata
- launch readiness verdict
- executive summary
- score and severity breakdown
- top remediation priorities
- findings table
- detailed finding structure
- sanitized evidence examples
- retest status language
- tested and not-tested scope
- limitations and disclaimer language
- final recommendation

It intentionally does not implement:

- scanner logic
- real report generation
- PDF generation
- backend report APIs
- database persistence
- authentication
- billing
- queue workers
- attack prompt library
- evaluator logic

## Demo Target

Fictional target app: **NovaDesk AI Support Copilot**

Target description:

- customer support RAG assistant
- fictional account lookup context
- fictional support workflow tools
- no real customer data
- no real secrets
- no real product scan

All account names, document names, canaries, dates, labels, and traces in the sample report are
fictional demo data.

## Reusable Report Content Structure

Future real reports should preserve this conceptual structure while keeping implementation details
separate from the static sample:

1. Cover and metadata
2. Demo or confidentiality labels where applicable
3. Launch readiness verdict
4. Executive summary
5. Security score and severity breakdown
6. Confidence summary
7. Tested categories
8. Top fixes
9. Findings table
10. Detailed findings
11. Sanitized evidence
12. Retest status
13. What was tested
14. What was not tested
15. Limitations and disclaimer
16. Final recommendation

Future report generation, if implemented in a later phase, should reference the methodology in
`docs/methodology.md` and should not treat this static document as executable schema. Phase 8 manual
report preparation should also reference `docs/audits/REPORT_DELIVERY.md`.

## Finding Content Pattern

Each detailed finding in the sample uses this structure:

- finding ID
- title
- category
- severity
- confidence
- status
- retest status
- plain-English description
- business impact
- evidence summary
- safe reproduction summary
- fix recommendation
- retest guidance

Evidence summaries should be useful for remediation while avoiding raw unsafe instructions, real
secrets, real customer data, long model transcripts, or exploit-ready prompt text.

## Demo Findings

The public sample report includes these fictional findings:

| ID | Title | Category | Severity | Confidence | Status |
| --- | --- | --- | --- | --- | --- |
| SHK-DEMO-001 | Cross-tenant RAG source returned in support answer | RAG data leakage | Critical | High | Open |
| SHK-DEMO-002 | Sensitive support tool action prepared without permission boundary | Tool/function abuse | High | Medium | Open |
| SHK-DEMO-003 | Retrieved article changed agent behavior through indirect instruction | Indirect prompt injection | High | Medium | Needs manual review |
| SHK-DEMO-004 | Generated answer rendered unsafe link treatment | Unsafe output handling | Medium | High | Open |
| SHK-DEMO-005 | Direct prompt injection bypassed support-topic boundary | Prompt injection | Medium | High | Fixed in sample retest |
| SHK-DEMO-006 | Retry loop allowed excessive model and retrieval calls | Cost abuse | Medium | Medium | Open |
| SHK-DEMO-007 | System instruction fragments appeared in refusal recovery | System prompt leakage | Low | Medium | Open |
| SHK-DEMO-008 | Source metadata exposed internal ticket labels | Sensitive data exposure | Low | High | Open |
| SHK-DEMO-009 | Retrieval source logging is insufficient for high-confidence retest | Evidence quality | Informational | Low | Inconclusive |
| SHK-DEMO-010 | Manual review recommended for destructive tool flows | Manual audit note | Informational | Low | Needs manual review |

Severity breakdown:

- Critical: 1
- High: 2
- Medium: 3
- Low: 2
- Informational: 2

Sample score: 64/100

Sample verdict: Not launch-ready

## Evidence Rules Used In The Sample

The sample report uses sanitized evidence only:

- fake account identifiers
- fake canary labels
- fictional support records
- shortened output excerpts
- no raw attack prompts
- no real secrets
- no real customer data
- no long model transcripts
- no customer logos
- no compliance badges
- no certification claims

The fake canary label `FAKE-CANARY-NOVA-042` is intentionally obvious demo data and should not be
used as a real secret or token.

## Retest Language

The sample report demonstrates these retest states:

- Not retested
- Failed retest
- Passed retest
- Partially fixed
- Inconclusive

Retesting should record the original scenario, retest date, changed controls, negative controls,
remaining limitations, and sanitized evidence. A finding should not be marked fixed without
retesting the documented issue path.

## Required Disclaimer Language

Future Sherlock reports should preserve the substance of this disclaimer:

Sherlock tests selected categories under defined assumptions. Passing a scan does not guarantee
complete security. Findings may require manual review. Severity depends on app context and business
impact. This report is not a compliance certification.

## Phase Boundary

Phase 4 completed the static sample report design only. Phase 5 adds an internal scanner engine foundation, Phase 6 adds an internal prompt library, Phase 7 adds an internal evaluator system, and Phase 8 adds a manual report delivery workflow. Real report generation, storage, PDF export, APIs, auth, billing, dashboards, admin panels, public scan execution, and worker systems remain future phases.
