# Report System

Status: Phase 18 Web Report foundation completed.

`packages/report_system` defines the internal data model and helper functions for PowerDetect Sherlock web reports. It consumes explicit, sanitized/static findings from `packages/findings_system` and produces a structured in-memory `Report` object for web UI and future API schema work.

Implemented:

- normalized report statuses: `draft`, `ready`, `needs_review`, `archived`
- report types: `web`, `sample`, `manual_audit`, `scan_summary`
- careful launch readiness verdicts without "secure", "safe", "certified", or "guaranteed" language
- conservative 0-100 score helper with caps for Critical, High, and needs-review findings
- severity breakdown helper
- top-fix selection by severity, confidence, business impact, and deduplicated fix recommendation
- findings table shaping
- detailed report finding formatting
- tested category formatting
- always-on limitations
- report-appropriate evidence formatting using Phase 17 redaction helpers
- builder that returns a structured `Report` object from explicit metadata and findings
- stdout-only CLI for schema/demo inspection

Not implemented:

- PDF export
- downloadable report assets
- billing gates
- paid plan enforcement
- active database persistence
- report database writes
- real report sharing tokens or public links
- report generation from real scans
- public scan execution
- raw sensitive evidence storage
- real customer evidence storage
- admin review workflow

Run the report system tests from the repository root:

```bash
python3 -m unittest discover -s packages/report_system/tests
```

Inspect the static schema contract:

```bash
python3 -m packages.report_system.cli
```

The CLI writes nothing to disk. Generated report artifacts, if future phases add them, must stay out of Git.
