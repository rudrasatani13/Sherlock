# Phase 2 Public Website

Status: completed

Phase 2 adds the public-facing website for PowerDetect Sherlock. The implementation is intentionally static and public-only so the product can communicate positioning, scope, trust language, and early access paths without adding scanner or platform surfaces too early.

## Implementation

Website path: `apps/web`

Pages:

- `index.html` - homepage
- `sample-report.html` - demo-only sample report page
- `methodology.html` - public methodology overview
- `security.html` - security and trust page
- `pricing.html` - pricing and early-access positioning
- `contact.html` - request audit, beta, and contact UI

Shared assets:

- `assets/styles.css`
- `assets/site.js`

## Local Preview

```bash
python3 -m http.server 4173 --directory apps/web
```

Open `http://localhost:4173/`.

## Scope Boundaries

Phase 2 does not implement:

- scanner logic
- attack prompt library
- evaluator logic
- backend API
- authenticated dashboard
- auth
- database
- billing or Stripe
- queue workers
- PDF generation
- real report generation
- target verification logic
- real scan execution

The sample report page is static demo content only. It is not generated from a real scan and should not be treated as a scanner output.

The contact form is frontend-only and opens a prefilled email draft. It does not submit to a backend or store form data.

## Phase 3 Follow-Up

The public website exposed the high-level categories and report shape that Phase 3 later formalized into internal methodology, severity taxonomy, evidence standards, remediation language, and limitations.

Phase 3 added `docs/methodology.md` as the detailed internal methodology and refreshed the public methodology page to stay aligned with that source of truth while remaining readable for website visitors.

## Phase 4 Follow-Up

Phase 4 replaced the short Phase 2 sample report positioning page with a fuller static demo report and added `docs/sample-report.md` as an internal reference. The page remains public demo content only and is not generated from scanner logic or customer data.
