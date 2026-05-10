# Web Report

Status: Phase 18 Web Report foundation completed.

Phase 18 adds Sherlock's web report foundation for PowerDetect Sherlock. It creates a structured report model, report section helpers, static API schema metadata, and a dashboard report detail shell that can consume sanitized static demo findings now and reviewed real findings later.

This phase prepares the product for Phase 19 PDF export, billing gates, sharing controls, and report persistence. Phase 19 now adds a separate PDF export foundation, but production customer PDF delivery is still not live.

## Scope

Implemented:

- report system package under `packages/report_system`
- structured report object model
- normalized report statuses: `draft`, `ready`, `needs_review`, `archived`
- normalized report types: `web`, `sample`, `manual_audit`, `scan_summary`
- launch readiness verdict helper
- conservative 0-100 security score helper
- severity breakdown helper
- top fixes helper
- findings table data shaping
- detailed finding section data shaping
- tested categories formatting
- not-tested and limitations helpers
- report-appropriate evidence formatting using Phase 17 findings-system redaction helpers
- builder from explicit sanitized/static Phase 17 finding objects
- stdout-only report system CLI for schema/demo inspection
- unit tests for report model, score, verdict, severity breakdown, top fixes, table shaping, tested categories, limitations, evidence formatting, and Phase 17 finding integration
- API `GET /api/v0/reports/schema` static metadata endpoint
- dashboard `apps/web/dashboard/reports.html` updates
- dashboard `apps/web/dashboard/report-detail.html` static web report shell

Not implemented by Phase 18:

- production customer PDF delivery
- public PDF download links
- downloadable customer report assets
- billing or Stripe
- paid plan gates
- public scan execution
- scanner execution from public UI/API
- production queue deployment
- active database persistence
- report database writes
- report generation from real customer scans
- real report sharing tokens
- public report links with access control
- admin panel
- real customer evidence storage
- raw sensitive evidence storage
- real network scanning
- production auth/session flow

## Package Structure

```text
packages/report_system/
|-- __init__.py
|-- builder.py
|-- cli.py
|-- evidence.py
|-- models.py
|-- scoring.py
|-- sections.py
|-- verdicts.py
|-- README.md
`-- tests/
    |-- __init__.py
    `-- test_report_system.py
```

## Report Model

The `Report` object includes:

- `report_id`
- `report_type`
- `title`
- `project_name`
- `target_name`
- `scan_type`
- `report_status`
- `generated_at`
- `launch_readiness_verdict`
- `security_score`
- `executive_summary`
- `severity_breakdown`
- `top_fixes`
- `findings`
- `tested_categories`
- `not_tested`
- `limitations`
- `evidence_handling_note`
- `retest_status`
- `methodology_version`
- `findings_system_version`
- `source_scan_id`
- `metadata`

The model is in-memory only in Phase 18. It is not saved to the Phase 10 database.

## Launch Readiness Verdicts

Allowed verdict values:

- `ready_with_low_risk`
- `needs_fixes_before_launch`
- `high_risk_do_not_launch`
- `manual_review_required`
- `inconclusive`

The verdict helper avoids final labels such as "secure", "safe", "certified", or "guaranteed". A verdict describes observed launch risk in the tested scope only.

## Security Score

The score helper returns a bounded score from 0 to 100.

Rules:

- no findings does not automatically mean 100
- Critical findings heavily reduce and cap score
- High findings materially reduce and cap score
- Medium findings reduce score
- Low and Informational findings reduce lightly
- `needs_review` findings cap score confidence
- false positives do not reduce score
- fixed findings retain only a small historical penalty

Score limitations are included in the returned `SecurityScore` object. The score is a communication aid, not a certification or guarantee.

## Findings Integration

Phase 18 consumes reviewed or demo `Finding` objects from `packages/findings_system`. The builder does not consume raw evaluator output directly unless the caller first passes that output through Phase 17 helpers.

The integration preserves:

- finding ID
- title
- category
- severity
- confidence
- status
- description
- business impact
- evidence summary
- evidence items
- reproduction steps
- fix recommendation
- manual review note
- source test IDs

Safe evaluator output does not automatically become report content. Phase 17 findings should be reviewed before customer-facing use.

## Evidence Handling

Report evidence must be:

- redacted
- short
- appropriate for report display
- free of raw headers
- free of raw cookies
- free of raw API keys
- free of bearer tokens
- free of private keys
- free of full private documents
- free of large transcripts
- free of real customer data

`packages/report_system.evidence` reuses Phase 17 redaction helpers and performs a best-effort sensitive-marker check before evidence is included in report snippets.

## Web UI

The Phase 18 dashboard UI is static:

- `apps/web/dashboard/reports.html`
- `apps/web/dashboard/report-detail.html`

The report detail shell includes:

- report summary header
- launch readiness verdict card
- security score card
- severity breakdown
- top fixes
- findings table
- detailed findings
- tested categories
- not-tested scope
- limitations
- evidence handling note
- retest status placeholders
- disabled export and sharing actions

The UI clearly states that it uses demo/static data only and does not include production PDF delivery, public sharing, production persistence, or real scan data.

## API Metadata

`GET /api/v0/reports/schema` returns static Phase 18 report contract metadata:

- report statuses
- report types
- launch readiness verdict values
- required fields
- score rules
- evidence rules
- disabled capabilities

`GET /api/v0/reports` remains a `501 not_implemented` placeholder for future customer report retrieval. It does not read or write database records.

## Phase 19 Connection

Phase 19 adds `packages/pdf_export`, static PDF export contract metadata, a local/demo print-ready HTML renderer, safety checks, and a disabled dashboard export placeholder. It consumes this Phase 18 `Report` object and keeps production delivery out of scope.

Do not add billing, public sharing links, active persistence, public scan execution, report database writes, raw evidence storage, real customer report retrieval, production PDF storage, or public PDF download links as part of the report foundation.
