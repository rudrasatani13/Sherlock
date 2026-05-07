# Scanner Engine

Status: Phase 5 Internal Scanner Engine V0 completed. Phase 6 prompt library, Phase 7 evaluator, Phase 8 manual audit workflow, and Phase 9 backend API boundary notes added.

Sherlock now includes the first internal scanner engine foundation under `packages/scanner_engine`. This is an internal execution layer for controlled local testing only. It is not exposed through the public website, backend APIs, dashboard, or any customer-facing scan flow.

## Phase 5 Scope

Phase 5 adds:

- target configuration format
- target adapter abstraction
- scan session creation
- basic scan lifecycle states: `pending`, `running`, `completed`, `failed`
- safe smoke test execution
- authorized target request dispatch through adapters
- local raw result capture
- local structured result JSON output
- local scan summary JSON output
- extension points for prompt library, evaluator, backend worker, and report phases

## Package Structure

```text
packages/scanner_engine/
|-- __init__.py
|-- adapters.py
|-- cli.py
|-- config.py
|-- example.scan.json
|-- models.py
|-- output.py
|-- prompts.py
|-- runner.py
`-- README.md
```

Responsibilities:

- `config.py` loads and validates internal scan config JSON.
- `models.py` defines scan sessions, tests, target responses, test results, run output, and summaries.
- `adapters.py` defines the target adapter interface plus `mock` and `http_api` implementations.
- `prompts.py` contains only safe smoke test fixtures for Phase 5.
- `runner.py` coordinates session lifecycle and test execution.
- `output.py` writes local JSON artifacts.
- `cli.py` provides an internal command-line entry point.

## Scan Config

The example config is `packages/scanner_engine/example.scan.json`. It intentionally uses a mock target and placeholder secret text only.

The config shape supports:

- target name
- target type
- endpoint URL for HTTP/API targets
- request method
- headers placeholder
- body/message field mapping
- scan mode
- max tests
- timeout
- notes
- output directory

Real secrets must not be committed. Real internal configs should be stored outside Git or in ignored local files.

## Target Adapters

Phase 5 includes:

- `mock`: safe local dry-run adapter with no network activity
- `http_api`: generic JSON HTTP/API adapter for authorized internal testing

Future target adapters can be added without changing scan lifecycle code:

- OpenAI-compatible endpoint adapter
- Vercel AI SDK endpoint adapter
- LangChain or LlamaIndex endpoint adapter
- browser chatbot adapter
- local runner adapter

## Scan Lifecycle

The runner creates a `ScanSession` with `pending` state, marks it `running`, executes selected safe smoke tests, and then marks it `completed` or `failed`.

No database is used. Session state and results live in memory during a run and are written to local JSON files at completion.

## Result Files

The default output directory is:

```text
scan-results/<scan_id>/
```

Each run writes:

- `raw-results.json`: raw per-test observations
- `scan-result.json`: structured scan object with target, tests, results, and extension point metadata
- `summary.json`: small run summary with counts and output paths

Generated scan output is ignored by Git and should not be committed.

## Safety Guardrails

- Internal use only.
- Run only against targets you own or are explicitly authorized to test.
- Do not scan third-party systems without permission.
- Do not put real secrets in committed configs.
- Treat outputs as sensitive because responses may contain private target data.
- Keep scan outputs protected and outside Git.
- Public scanning must not be added until ownership verification, SSRF protection, rate limits, spend controls, logging controls, and abuse prevention exist.

## Phase 6 Prompt Library Connection

Phase 6 adds `packages/prompt_library`, a versioned internal attack prompt/test-case library. The library includes stable IDs, categories, versions, intended safe behavior, failure signals, safety notes, target type metadata, and context setup notes.

The Phase 5 scanner runner still defaults to `safe_smoke` mode and benign smoke prompts. It does not automatically execute the attack prompt library. Future scanner work can call `packages.prompt_library.select_test_cases()` and convert selected cases to `ScannerTest` objects with prompt metadata attached.

## Phase 7 Evaluator Connection

Phase 7 adds the local evaluator package under `packages/evaluator_system`. It consumes structured test results after target responses are captured and classifies observations into deterministic evaluation results with verdicts, severity, confidence, evidence snippets, redacted evidence, and manual-review flags.

The scanner engine deliberately records placeholder fields such as `severity: not_assigned_by_scanner_engine` and `evaluation_status: not_evaluated_by_scanner_engine` rather than performing vulnerability detection inside the runner.

## Phase 8 Manual Audit Workflow Connection

Phase 8 adds the human-led workflow under `docs/audits`. In that workflow, the scanner can be run only after intake, written authorization, approved scope, testing windows, rate limits, and data-handling rules are confirmed.

Scanner outputs remain local observations under ignored `scan-results/`. They should be reviewed with the Phase 7 evaluator and manual playbooks before any customer-facing finding is drafted.

## Future Backend and Worker Connection

Future backend APIs and queue workers should treat the scanner engine as an isolated execution module. A backend can validate authorization and create scan jobs, while a worker can load a scan config, execute the runner, store outputs, and hand structured results to evaluator/report systems.

Phase 9 adds a backend API foundation under `apps/api`, but it does not expose scanner execution. The scanner must remain inaccessible from public request handlers until future phases add auth, authorization, ownership verification, SSRF protection, rate limits, spend controls, audit logging, and queue workers.
