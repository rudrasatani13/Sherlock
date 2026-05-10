# Sherlock Web

Status: Phase 18 Web Report dashboard foundation completed.

This directory contains the static public website, Phase 12 Dashboard V0 + Auth UI Shell, Phase 13 Project Target Setup UI, Phase 14 Target Verification UI, Phase 16 Scan Types + Limits UI, Phase 17 static findings UI copy, and Phase 18 static web report UI shell for PowerDetect Sherlock.

It is intentionally static:

- no backend routes inside this app
- no scanner execution
- no production authentication/session flow
- no database
- no real project or target persistence
- no production target ownership verification checks
- no billing
- no production queue workers (local queue/worker foundation exists under `packages/worker_system`)
- no active findings persistence or real findings API consumption
- no report generation from real scans
- no report persistence
- no public report sharing
- no PDF export
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
- `dashboard/projects.html` - Phase 13 projects page with setup CTA, empty state, demo project cards, and target metadata table
- `dashboard/project-setup.html` - Phase 13 static project setup form
- `dashboard/project-detail.html` - Phase 13 static project detail placeholder
- `dashboard/target-setup.html` - Phase 13 static target setup form
- `dashboard/target-detail.html` - Phase 13 static target detail placeholder
- `dashboard/target-verification.html` - Phase 14 target ownership verification page with method selector, instructions, status, and security boundaries
- `dashboard/scan-setup.html` - Phase 16 static scan setup page displaying scan types, limits, and plan tier tables with disabled execution controls
- `dashboard/scans.html` - static scans page with lifecycle status examples and link to scan setup
- `dashboard/findings.html` - static Phase 17 findings page with demo-only structure, statuses, evidence boundaries, and disabled filters/actions
- `dashboard/reports.html` - Phase 18 static reports page linking to the dashboard web report shell and public sample report
- `dashboard/report-detail.html` - Phase 18 static web report detail shell with verdict, score, severity breakdown, top fixes, findings table, detailed findings, tested categories, not-tested scope, limitations, evidence note, and disabled export/share actions
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
http://localhost:4173/dashboard/project-setup.html
http://localhost:4173/dashboard/target-setup.html
http://localhost:4173/dashboard/target-verification.html
http://localhost:4173/dashboard/scan-setup.html
http://localhost:4173/dashboard/report-detail.html
```

The contact form opens a prefilled email draft. It does not submit to a backend or store data.

The auth UI forms are frontend-only and show "not connected yet" messages on submit. They do not create accounts, create sessions, send reset emails, store tokens, or store credentials. The login and settings pages can optionally fetch `http://localhost:8000/api/v0/auth/status` when the local API is running; this endpoint returns configuration state only.

The Phase 13 setup forms validate required fields in the browser and update local previews only. They do not submit project or target data to the API, write database records, verify ownership, store secrets, or run scans. Auth fields are placeholders for future secure handling; do not paste real API keys, bearer tokens, cookies, passwords, private keys, raw headers, or production credentials into the static UI.

The Phase 14 target verification page displays verification method selection, challenge instructions, and status cards. It does not issue real challenges, perform DNS/HTTP/chatbot checks, persist verification records, or unlock scanning. The "Verify Target" button is disabled. Method-specific instructions toggle via browser-side JavaScript only.

Phase 3 refreshed `methodology.html` to align with the internal methodology in `../../docs/methodology.md`. The public page remains a readable overview, not the full internal taxonomy and not an attack prompt library.

Phase 4 expands `sample-report.html` into a realistic static sample report with fictional findings, sanitized demo evidence, retest status, limitations, and final recommendations. Phase 6 adds an internal prompt library outside the web app under `../../packages/prompt_library`. Phase 8 adds manual audit workflow documentation under `../../docs/audits`. Phase 9 adds a separate backend API foundation under `../api`. Phase 11 adds backend auth placeholders. Phase 12 adds the dashboard/auth UI shell. Phase 13 adds project and target setup UI only. Phase 14 adds the target ownership verification page and updates existing project/target pages with verification links and status. Phase 16 adds a static scan setup page that displays scan types and limits without running any scans. Phase 17 updates the static findings page to reflect the internal findings model, statuses, evidence boundaries, and future review workflow without connecting it to a backend. Phase 18 adds the static dashboard report detail shell and report list updates using demo data only.

The web app is still not generated from a real scan and does not implement report generation from real scans, PDF export, protected API consumption, production auth, database storage, findings persistence, report persistence, public report sharing, real customer evidence storage, billing, Stripe, queue workers, scanner logic, prompt execution, evaluator code, admin panels, production verification checks, project persistence, target persistence, scan creation, or public self-serve scanning.
