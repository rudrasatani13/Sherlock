# Findings System

Status: Phase 17 Findings System foundation completed.

Phase 17 adds Sherlock's internal findings system under `packages/findings_system`. It converts safe Phase 7 evaluator output into structured finding candidates and finalized finding objects for review. It prepares the data contract needed for Phase 18 web reports, but it does not build the web report.

## Scope

Implemented:

- finding candidate model for evaluator-derived observations
- finalized finding model with title, category, severity, confidence, status, description, business impact, evidence, reproduction steps, fix recommendation, source IDs, evaluator signals, duplicate group key, manual review placeholders, timestamps, and metadata
- normalized status definitions: `open`, `fixed`, `accepted_risk`, `false_positive`, `needs_review`
- severity and confidence validation aligned to `docs/methodology.md`
- category mapping from methodology, prompt library, scan limits, and evaluator signal names
- duplicate grouping for same category, target, detector, and evidence signal
- merge helpers that preserve strongest severity/confidence, source test IDs, redacted evidence summaries, evaluator signals, and merge metadata
- sorting by severity, confidence, category, and title
- evidence redaction and short summary helpers
- recommendation templates by category
- adapter from Phase 7 evaluator output to finding candidates
- local CLI for safe/mock evaluator JSON conversion
- unit tests for model validation, status/severity/confidence, category mapping, evidence redaction, grouping, merging, sorting, recommendation selection, and evaluator adapter behavior
- static API schema metadata at `GET /api/v0/findings/schema`
- static dashboard findings page copy aligned to Phase 17

Not implemented:

- Phase 18 web report
- report generation
- PDF export
- public scan execution
- scanner execution from public UI or API routes
- production queue deployment
- billing or Stripe
- admin panel
- active database persistence
- findings database reads or writes
- real customer evidence storage
- raw sensitive evidence storage
- production dashboard API integration
- real network scanning
- LLM-as-judge behavior

## Finding Candidate

A `FindingCandidate` is a lightweight observation that may still need human review. It can include:

- `category`
- `detector_name`
- `severity_hint`
- `confidence_hint`
- `observed_behavior`
- `evidence_snippet`
- `redacted_evidence`
- `test_case_id`
- `needs_manual_review`
- `reason`
- `affected_target`
- `source_scan_id`
- `source_test_ids`
- `evaluator_signals`
- `metadata`

Candidates are not customer-facing findings. They preserve evaluator context while keeping evidence redacted.

## Final Finding

A finalized `Finding` includes:

- `finding_id`
- `title`
- `category`
- `severity`
- `confidence`
- `status`
- `description`
- `business_impact`
- `evidence_summary`
- `evidence_items`
- `reproduction_steps`
- `fix_recommendation`
- `affected_target`
- `source_scan_id`
- `source_test_ids`
- `evaluator_signals`
- `duplicate_group_key`
- `manual_review_required`
- `manual_review_notes`
- `accepted_risk_reason`
- `false_positive_reason`
- `created_at`
- `updated_at`
- `metadata`

The object is in-memory only in Phase 17. It is not saved to the Phase 10 database.

## Categories

Normalized Phase 17 categories:

- `prompt_injection`
- `system_prompt_leakage`
- `sensitive_data_leakage`
- `rag_data_leakage`
- `indirect_prompt_injection`
- `tool_function_abuse`
- `unsafe_output_handling`
- `cost_abuse_unbounded_consumption`
- `other_unknown`

Existing internal names are mapped into this contract. For example, Phase 6 and Phase 16 use `cost_abuse`, while Phase 17 normalizes it to `cost_abuse_unbounded_consumption`. Evaluator groups such as `sensitive_data_pattern` and `canary_token_leakage` also map into methodology categories.

## Validation Rules

- Category must be known or safely normalized to `other_unknown`.
- Severity must be `critical`, `high`, `medium`, `low`, or `informational`.
- Confidence must be `high`, `medium`, or `low`.
- Status must be `open`, `fixed`, `accepted_risk`, `false_positive`, or `needs_review`.
- Critical and high findings require a non-empty evidence summary.
- Critical and high findings require a fix recommendation.
- Critical and high findings require strong evidence or manual review.
- Evidence is redacted by default.
- Finding titles and descriptions must be specific enough for non-security developers.
- `false_positive` requires a reason.
- `accepted_risk` supports a future review note or reason field through `accepted_risk_reason`.

## Evidence Rules

Evidence summaries should be short, redacted, and report-safe. They should not include:

- raw headers
- raw cookies
- raw API keys
- bearer tokens
- private keys
- full private documents
- large model transcripts
- real customer data

The findings package reuses the Phase 7 evaluator redaction helper and adds extra header, cookie, private-document, and length controls.

## Grouping, Merge, and Sort

Duplicate grouping uses:

- normalized category
- affected target
- detector or title signal
- similar observed behavior or evidence fingerprint

Merging preserves:

- strongest severity
- strongest confidence
- combined source test IDs
- redacted evidence summaries
- evaluator signals
- manual review requirement
- merge metadata

Findings sort by:

1. severity: `critical`, `high`, `medium`, `low`, `informational`
2. confidence: `high`, `medium`, `low`
3. category
4. title

## Recommendations

Phase 17 includes simple fix recommendation templates for prompt injection, system prompt leakage, sensitive data leakage, RAG data leakage, indirect prompt injection, tool/function abuse, unsafe output handling, cost abuse/unbounded consumption, and unknown categories.

Recommendations are practical guidance, not proof that the issue will be fully remediated.

## API and Dashboard

`GET /api/v0/findings` remains a `501 not_implemented` placeholder. It includes Phase 17 contract metadata but does not read or write findings.

`GET /api/v0/findings/schema` returns static metadata for statuses, severities, confidences, categories, required fields, validation rules, and disabled capabilities. It does not return real customer findings or evidence.

`apps/web/dashboard/findings.html` remains a static demo page. It shows the Phase 17 structure and statuses but is not connected to backend findings, a database, scan execution, reports, or PDF export.

## Local CLI

Convert safe/mock evaluator output to stdout:

```bash
python3 -m packages.findings_system.cli --input path/to/evaluation.json
```

Generated findings output should stay out of Git. Do not commit generated reports, scan outputs, evaluator outputs, logs, or sensitive files.
