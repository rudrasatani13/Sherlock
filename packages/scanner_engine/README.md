# Internal Scanner Engine V0

Status: Phase 5 internal foundation. Phase 6 prompt library, Phase 7 evaluator system, Phase 8 manual audit workflow, and Phase 9 backend API foundation are available separately.

This package contains the first internal scanner engine foundation for PowerDetect Sherlock. It is not a public product feature and should only be run against targets you are authorized to test.

## What Phase 5 Adds

- scan configuration loading and validation
- scan session creation with `pending`, `running`, `completed`, and `failed` states
- target adapter abstraction
- mock target adapter for safe local dry-runs
- generic HTTP/API target adapter for authorized internal testing
- small safe smoke test set
- local JSON output for raw results, structured scan result, and summary
- extension points for the Phase 6 prompt library and Phase 7 evaluator integration

## What Is Not Implemented Here

- prompt library execution by default
- vulnerability detection inside the scanner runner
- severity scoring inside the scanner runner
- database persistence
- backend scan APIs
- dashboard integration
- authentication
- billing
- queue workers
- PDF generation
- public scan execution
- admin panel
- target ownership verification
- SSRF protection
- browser automation scanning
- CI/GitHub integration

## Safe Local Dry-Run

From the repository root:

```bash
python3 -m packages.scanner_engine.cli --config packages/scanner_engine/example.scan.json
```

The example config uses the mock adapter and does not make network requests.

## Authorized HTTP/API Target Shape

The `http_api` adapter is intentionally minimal. It sends each safe smoke test input to a configured endpoint using the configured method, headers, and body mapping. Only use it for systems you own or are explicitly authorized to test.

No real secrets should be added to config files. Use local ignored files for real internal configs, and keep generated output protected.

## Output

The default output directory is `scan-results/<scan_id>/`.

Each run writes:

- `raw-results.json`
- `scan-result.json`
- `summary.json`

The repository `.gitignore` excludes `scan-results/` and related generated scan/report folders.

## Future Extension Points

Phase 6 adds `../prompt_library`, a versioned prompt library that supplies reviewed scenario definitions. This runner still defaults to safe smoke tests and does not automatically execute the attack prompt library.

Phase 7 adds `../evaluator_system`, which can evaluate scanner output after execution and transform raw observations into classified local evaluation results only when deterministic evidence requirements are met.

Phase 8 adds the manual audit workflow under `../../docs/audits`, which explains how scanner observations should be authorized, reviewed, redacted, converted into findings, delivered, retested, and closed by a human auditor.

Future backend, worker, report, and PDF phases should call the scanner engine through explicit contracts instead of coupling UI code to scanner internals.

Phase 9 adds API placeholders only and does not expose scanner execution through HTTP routes.

## Safety Notes

- Internal use only.
- Scan only authorized targets.
- Do not scan third-party systems without permission.
- Do not store real secrets in committed configs.
- Generated outputs may contain sensitive prompts, responses, headers, or target data.
- Protect and delete scan outputs according to the target's data handling requirements.
- SSRF protection and ownership verification are not implemented in Phase 5 and must be added before any public scanning feature exists.
