# Evaluator System V0

Status: Phase 7 internal foundation. Phase 8 manual audit workflow and Phase 9 backend API foundation are available separately.

This package contains the first deterministic evaluator system for PowerDetect Sherlock. It evaluates Phase 5 scanner results and Phase 6 prompt-library metadata locally, then produces structured verdicts, severities, confidence levels, evidence snippets, redacted evidence, and manual-review flags.

## What Phase 7 Adds

- stdlib-only evaluator package
- deterministic rule-based detectors
- result schemas for evaluation input, evidence, matched signals, and evaluation output
- evidence snippet extraction and redaction helpers
- canary token leakage detection
- sensitive-data-pattern detection
- system-prompt-leakage detection
- unsafe-output detection
- tool/function-abuse detection
- cost-abuse detection
- prompt-library failure-signal exact matching
- local CLI for evaluating scanner result JSON files
- unittest validation coverage

## What Is Not Implemented

- backend APIs
- database persistence
- authentication
- billing
- dashboard integration
- queue workers
- PDF generation
- public scanning
- admin panel
- browser automation
- LLM-as-judge behavior
- machine-learning classifiers
- real report generation

## Local Usage

Evaluate a Phase 5 `scan-result.json` file and write output under ignored `scan-results/evaluations/`:

```bash
python3 -m packages.evaluator_system.cli --input scan-results/<scan_id>/scan-result.json
```

Print evaluation JSON to stdout instead:

```bash
python3 -m packages.evaluator_system.cli --input scan-results/<scan_id>/scan-result.json --stdout
```

Run tests:

```bash
python3 -m unittest packages.evaluator_system.tests.test_evaluator
```

## Output Shape

Each evaluation result includes:

- `test_id`
- `category`
- `verdict`
- `severity`
- `confidence`
- `matched_signals`
- `evidence`
- `reasoning_summary`
- `needs_manual_review`
- `manual_review_reasons`
- `evaluator_version`
- `evaluated_at`
- `error`

Valid verdicts are `safe`, `suspicious`, `vulnerable`, `needs_manual_review`, `inconclusive`, and `error`.

Valid severities are `critical`, `high`, `medium`, `low`, `informational`, and `none`.

Valid confidence values are `high`, `medium`, `low`, and `none`.

## Safety Notes

The evaluator is local and internal. It may process scanner responses that contain sensitive target data. Generated outputs should remain in ignored folders and should be handled with the same care as raw scan outputs.

The evaluator is conservative and explainable. It should not be treated as proof that a system is secure, and high-impact or low-confidence findings should receive manual review before customer-facing reporting.

Phase 8 documents that manual review process under `../../docs/audits`, including finding review, severity/confidence review, report delivery, retesting, and audit closure.

Phase 9 API placeholders do not run evaluator code, persist evaluator output, generate findings, or generate reports.
