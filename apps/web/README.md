# Sherlock Public Website

This directory contains the static public website for PowerDetect Sherlock.

It is intentionally static:

- no backend routes
- no scanner execution
- no authentication
- no database
- no billing
- no report generation
- no admin panel
- no public self-serve scanning

## Pages

- `index.html` - homepage and product positioning
- `sample-report.html` - polished Phase 4 demo-only sample report
- `methodology.html` - public methodology overview
- `security.html` - public trust and scanning safety notes
- `pricing.html` - early access and future offer positioning
- `contact.html` - frontend-only audit, beta, and contact flow

## Local Preview

From the repository root:

```bash
python3 -m http.server 4173 --directory apps/web
```

Then open:

```text
http://localhost:4173/
```

The contact form opens a prefilled email draft. It does not submit to a backend or store data.

Phase 3 refreshed `methodology.html` to align with the internal methodology in `../../docs/methodology.md`. The public page remains a readable overview, not the full internal taxonomy and not an attack prompt library.

Phase 4 expands `sample-report.html` into a realistic static sample report with fictional findings, sanitized demo evidence, retest status, limitations, and final recommendations. Phase 6 adds an internal prompt library outside the web app under `../../packages/prompt_library`. Phase 8 adds manual audit workflow documentation under `../../docs/audits`. The public website is still not generated from a real scan and does not implement report generation, PDF export, APIs, auth, database storage, billing, scanner logic, prompt execution, evaluator code, admin panels, or public self-serve scanning.
