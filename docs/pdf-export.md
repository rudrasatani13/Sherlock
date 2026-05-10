# PDF Report Export

Status: Phase 19 PDF Report Export foundation completed.

Phase 19 prepares PowerDetect Sherlock to export polished PDF reports from structured Phase 18 `Report` objects. It is a foundation only: the repo now has a PDF export contract, print-ready HTML template path, safety checks, local/demo CLI, static dashboard placeholder, and static API schema metadata.

## Scope

Implemented:

- `packages/pdf_export` package
- normalized export statuses: `draft`, `ready`, `blocked_sensitive_evidence`, `failed`, `archived`
- export types: `pdf`, `print_html`, `preview`
- export data contract with cover page, executive summary, launch readiness verdict, score, severity breakdown, top fixes, findings table, detailed findings, evidence snippets, reproduction steps, fix recommendations, tested categories, not-tested scope, limitations, evidence handling note, footer disclaimer, source report ID, and metadata
- builder from Phase 18 `Report` objects
- print-ready HTML renderer suitable for local browser print-to-PDF
- local/demo CLI that defaults to stdout and writes only to ignored directories when explicitly requested
- safe filename generation with the `powerdetect-sherlock-report-` prefix
- output path validation for `pdf-output/`, `pdf-exports/`, and `report-exports/`
- evidence safety checks for raw Authorization headers, cookies, API keys, bearer tokens, private keys, full private documents, large transcripts, and secret-like markers
- verdict overclaiming checks
- dashboard report detail button placeholder labeled as the Phase 19 foundation
- static API `GET /api/v0/reports/schema` PDF export contract metadata

Not implemented:

- production PDF export for real customer reports
- public PDF download links
- public report sharing
- billing or Stripe
- live paid-plan gates
- active report database persistence
- report database writes
- file upload or production storage integration
- S3 or Supabase Storage integration
- email delivery
- admin panel
- public scan execution
- scanner execution from public UI/API
- real network scanning
- raw sensitive evidence storage
- real customer evidence storage
- Phase 20 retest flow

## Package Structure

```text
packages/pdf_export/
|-- __init__.py
|-- cli.py
|-- models.py
|-- renderer.py
|-- safety.py
|-- template.py
|-- README.md
`-- tests/
    |-- __init__.py
    `-- test_pdf_export.py
```

## Export Model

The `PdfReportExport` object includes:

- `export_id`
- `report_id`
- `export_status`
- `export_type`
- `title`
- `filename`
- `generated_at`
- `cover_page`
- `executive_summary`
- `verdict`
- `score`
- `severity_breakdown`
- `top_fixes`
- `findings_table`
- `detailed_findings`
- `tested_categories`
- `not_tested`
- `limitations`
- `evidence_handling_note`
- `footer_disclaimer`
- `source_report_id`
- `metadata`

The model is in-memory unless the CLI is explicitly asked to write a local ignored HTML artifact.

## Template and Renderer

Phase 19 uses a dependency-light print-ready HTML renderer instead of adding a PDF library. This keeps the current static/foundation direction intact while preserving the future PDF template structure.

The renderer includes:

1. Cover page
2. Executive summary
3. Launch readiness verdict
4. Security score
5. Severity breakdown
6. Top fixes
7. Findings table
8. Detailed findings
9. Evidence snippets
10. Reproduction steps
11. Fix recommendations
12. Tested categories
13. Not-tested scope
14. Limitations
15. Evidence handling note
16. Retest status placeholder

The CLI can print schema/demo output to stdout or write print-ready HTML locally:

```bash
python3 -m packages.pdf_export.cli
python3 -m packages.pdf_export.cli --demo
python3 -m packages.pdf_export.cli --render-html
python3 -m packages.pdf_export.cli --write-html --output-dir pdf-exports
```

Generated artifacts must stay in ignored directories and must not be committed.

## Evidence Safety

PDF-safe evidence must be:

- redacted
- short
- report-safe
- free of raw headers
- free of raw cookies
- free of API keys
- free of bearer tokens
- free of private keys
- free of full private documents
- free of large transcripts
- free of real customer data

The Phase 19 package reuses the Phase 17 findings evidence checks and the Phase 18 report-safe evidence flow. It blocks export objects when evidence contains unredacted secret-like markers, raw Authorization headers, raw cookies, private key markers, private document markers, overclaiming verdict language, missing limitations, unsafe filenames, or path traversal.

## Storage and Download Planning

Future production PDF delivery must add:

- authenticated report access
- organization-scoped authorization
- active report persistence
- secure server-side artifact generation
- private storage with signed short-lived access where appropriate
- audit logging
- retention and deletion rules
- paid-plan enforcement if PDF export becomes a paid feature

Phase 19 does not implement those behaviors. It only defines the contract and local/demo rendering foundation.

## Tests

Run:

```bash
python3 -m unittest discover -s packages/pdf_export/tests
```

The tests cover model validation, export status validation, safe filename generation, path traversal rejection, output directory safety, evidence safety checks, overclaiming verdict rejection, limitations requirement, template section generation, Phase 18 report integration, CLI dry-run schema behavior, and local HTML write safety.
