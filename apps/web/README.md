# Sherlock Web

This directory contains the static public website and Phase 12 Dashboard V0 + Auth UI Shell for PowerDetect Sherlock.

It is intentionally static:

- no backend routes inside this app
- no scanner execution
- no production authentication/session flow
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
- `login.html` - Phase 12 login UI shell
- `signup.html` - Phase 12 signup UI shell
- `forgot-password.html` - Phase 12 password reset UI shell
- `dashboard/index.html` - Phase 12 dashboard overview shell
- `dashboard/projects.html` - static projects page with empty/demo states
- `dashboard/scans.html` - static scans page with lifecycle status examples
- `dashboard/findings.html` - static findings page with severity/filter placeholders
- `dashboard/reports.html` - static reports page linking to the sample report
- `dashboard/settings.html` - static account/settings page with auth-status placeholder

## Local Preview

From the repository root:

```bash
python3 -m http.server 4173 --directory apps/web
```

Then open:

```text
http://localhost:4173/
http://localhost:4173/login.html
http://localhost:4173/dashboard/
```

The contact form opens a prefilled email draft. It does not submit to a backend or store data.

The auth UI forms are frontend-only and show "not connected yet" messages on submit. They do not create accounts, create sessions, send reset emails, store tokens, or store credentials. The login and settings pages can optionally fetch `http://localhost:8000/api/v0/auth/status` when the local API is running; this endpoint returns configuration state only.

Phase 3 refreshed `methodology.html` to align with the internal methodology in `../../docs/methodology.md`. The public page remains a readable overview, not the full internal taxonomy and not an attack prompt library.

Phase 4 expands `sample-report.html` into a realistic static sample report with fictional findings, sanitized demo evidence, retest status, limitations, and final recommendations. Phase 6 adds an internal prompt library outside the web app under `../../packages/prompt_library`. Phase 8 adds manual audit workflow documentation under `../../docs/audits`. Phase 9 adds a separate backend API foundation under `../api`. Phase 11 adds backend auth placeholders. Phase 12 adds the dashboard/auth UI shell only.

The web app is still not generated from a real scan and does not implement report generation, PDF export, protected API consumption, production auth, database storage, billing, scanner logic, prompt execution, evaluator code, admin panels, target verification, project persistence, scan creation, or public self-serve scanning.
