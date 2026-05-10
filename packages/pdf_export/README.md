# PDF Export

Status: Phase 19 PDF Report Export foundation completed.

`packages/pdf_export` prepares PowerDetect Sherlock to export polished PDF reports from structured Phase 18 `Report` objects. The current implementation is dependency-light and renders print-ready HTML for local/demo use only.

Implemented:

- normalized export statuses: `draft`, `ready`, `blocked_sensitive_evidence`, `failed`, `archived`
- export types: `pdf`, `print_html`, `preview`
- PDF export data contract with cover page, executive summary, verdict, score, findings, evidence, fixes, tested categories, not-tested scope, limitations, evidence handling, footer disclaimer, and metadata
- builder from Phase 18 `Report` objects
- PDF-safe evidence validation using Phase 17/18 redaction behavior
- safe filename generation with the `powerdetect-sherlock-report-` prefix
- path traversal rejection and allowed local output directories
- print-ready HTML renderer suitable for browser print-to-PDF
- CLI for schema/demo inspection and optional local ignored HTML artifact generation

Not implemented:

- production PDF export for real customer reports
- public PDF download links
- public report sharing
- billing or Stripe
- live paid-plan gates
- active report database persistence
- report database writes
- production storage integration
- email delivery
- admin panel
- real customer evidence storage
- public scan execution
- Phase 20 retest flow

Allowed local artifact directories:

- `pdf-output/`
- `pdf-exports/`
- `report-exports/`

Generated PDF/HTML exports must stay out of Git.

Run tests:

```bash
python3 -m unittest discover -s packages/pdf_export/tests
```

Inspect the static contract:

```bash
python3 -m packages.pdf_export.cli
```

Print a demo export object:

```bash
python3 -m packages.pdf_export.cli --demo
```

Render print-ready HTML to stdout:

```bash
python3 -m packages.pdf_export.cli --render-html
```

Write a local ignored print-ready HTML artifact:

```bash
python3 -m packages.pdf_export.cli --write-html --output-dir pdf-exports
```
