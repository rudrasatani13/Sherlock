# Findings System

Status: Phase 17 Findings System foundation completed.

This package converts Phase 7 evaluator observations into structured finding candidates and finalized finding objects for internal review. It is stdlib-only and does not persist data, generate reports, export PDFs, run scans, call external AI services, or store raw customer evidence.

## Package Shape

```text
packages/findings_system/
|-- __init__.py
|-- categories.py
|-- cli.py
|-- evidence.py
|-- grouping.py
|-- models.py
|-- normalizer.py
|-- recommendations.py
|-- severity.py
|-- statuses.py
|-- README.md
`-- tests/
    |-- __init__.py
    `-- test_findings_system.py
```

## Finding Fields

Finalized findings include:

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

## Statuses

Phase 17 finalized findings normalize to exactly:

- `open`
- `fixed`
- `accepted_risk`
- `false_positive`
- `needs_review`

Future status names such as `inconclusive`, `duplicate`, and `retest_required` are contract notes only. Existing database docs use `needs_manual_review`; this package maps that alias to `needs_review` for the Phase 17 contract.

## Categories

Phase 17 normalizes findings into:

- `prompt_injection`
- `system_prompt_leakage`
- `sensitive_data_leakage`
- `rag_data_leakage`
- `indirect_prompt_injection`
- `tool_function_abuse`
- `unsafe_output_handling`
- `cost_abuse_unbounded_consumption`
- `other_unknown`

Existing package names such as `cost_abuse`, evaluator groups such as `sensitive_data_pattern`, and manual-review aliases are mapped into the normalized categories.

## Safety Rules

- Critical and high findings require an evidence summary.
- Critical and high findings require fix guidance.
- Critical severity requires strong evidence or manual review.
- Evidence is redacted and shortened by default.
- Raw headers, cookies, API keys, private keys, bearer tokens, and large raw transcripts should not be stored in finding objects.
- `false_positive` requires a reason.

## Local CLI

Convert a safe/mock evaluator JSON file to stdout:

```bash
python3 -m packages.findings_system.cli --input path/to/evaluation.json
```

Optional output files should stay in ignored local folders. Do not commit generated findings, scan outputs, reports, logs, or sensitive evidence.
