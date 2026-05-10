# Prompt Library

Status: Phase 6 Attack Prompt Library V0 completed. Phase 7 evaluator system is available separately under `packages/evaluator_system`. Phase 9 backend API foundation does not expose prompt execution.

Sherlock now includes the first internal attack/test prompt library under `packages/prompt_library`. The library is for controlled authorized testing and future scanner/evaluator integration. It is not exposed through the public website, backend APIs, dashboard, or customer-facing scan flows.

## Purpose

The Phase 6 prompt library provides reviewed, versioned, categorized test cases for the Phase 3 methodology categories:

- Prompt Injection
- System Prompt Leakage
- Sensitive Data Leakage
- RAG Data Leakage / Document Exfiltration
- Indirect Prompt Injection
- Tool / Function Abuse
- Unsafe Output Handling
- Cost Abuse / Unbounded Consumption

The library records test intent, input text, expected safe behavior, failure signals, context requirements, target types, and safety notes. It does not decide whether a target is vulnerable.

## Package Structure

```text
packages/prompt_library/
|-- manifest.json
|-- schema/test-case.schema.json
|-- categories/
|   |-- prompt_injection.json
|   |-- system_prompt_leakage.json
|   |-- sensitive_data_leakage.json
|   |-- rag_data_leakage.json
|   |-- indirect_prompt_injection.json
|   |-- tool_function_abuse.json
|   |-- unsafe_output_handling.json
|   `-- cost_abuse.json
|-- loader.py
|-- validate.py
|-- __init__.py
`-- README.md
```

## Schema Fields

Each test case includes:

- `id`: stable test-case ID, such as `SHK-APL-PI-001`
- `version`: semantic version for the case
- `category`: machine-readable methodology category
- `title`: short human-readable name
- `description`: what the test is checking
- `input`: the user prompt or test input to send to a target
- `tags`: searchable metadata labels
- `severity_hint`: non-binding evaluator/reporting hint
- `expected_behavior`: safe behavior the target should show
- `failure_signals`: observable signals an evaluator or reviewer can inspect
- `safety_notes`: why the case is safe and how it avoids real harm
- `requires_context`: whether synthetic fixture context is needed
- `context_setup`: fake/demo setup notes when needed
- `target_types`: target families where the case is relevant
- `status`: `enabled`, `disabled`, or `experimental`
- `enabled`: execution-selection flag
- `references`: methodology or documentation references

Allowed `severity_hint` values are `critical`, `high`, `medium`, `low`, and `informational`. Severity hints are not final finding severity.

Allowed target types are `generic_chat`, `api_endpoint`, `rag`, `agent`, `tool_using_agent`, `openai_compatible`, `vercel_ai_sdk`, `langchain`, and `llamaindex`.

## Category Counts

Phase 6 V0 contains 88 test cases:

| Category | File | Count |
| --- | --- | ---: |
| Prompt Injection | `categories/prompt_injection.json` | 18 |
| System Prompt Leakage | `categories/system_prompt_leakage.json` | 12 |
| Sensitive Data Leakage | `categories/sensitive_data_leakage.json` | 10 |
| RAG Data Leakage / Document Exfiltration | `categories/rag_data_leakage.json` | 12 |
| Indirect Prompt Injection | `categories/indirect_prompt_injection.json` | 10 |
| Tool / Function Abuse | `categories/tool_function_abuse.json` | 10 |
| Unsafe Output Handling | `categories/unsafe_output_handling.json` | 10 |
| Cost Abuse / Unbounded Consumption | `categories/cost_abuse.json` | 6 |

## Loader and Validation

Validate the library from the repository root:

```bash
python3 -m packages.prompt_library.validate
```

The validator confirms:

- category files parse as JSON
- required fields are present
- test-case IDs are unique
- category counts match the manifest
- severity hints, statuses, and target types use supported values
- context setup is present when `requires_context` is true

Load cases in Python:

```python
from packages.prompt_library import load_prompt_library, select_test_cases

library = load_prompt_library()
all_enabled = library.enabled_cases()
rag_cases = select_test_cases(categories=["rag_data_leakage"], target_types=["rag"])
scanner_tests = library.to_scanner_tests(max_tests=5)
```

`to_scanner_tests()` converts enabled prompt-library cases into the Phase 5 scanner engine's `ScannerTest` shape with metadata attached. The Phase 5 runner still defaults to `safe_smoke` tests and does not automatically run the attack prompt library.

## Scanner Engine Integration Notes

Phase 5 scanner tests currently use:

- `test_id`
- `category`
- `input`
- `metadata`

Phase 6 prompt test cases map cleanly into this shape:

- `id` maps to `test_id`
- `category` maps to `category`
- `input` maps to `input`
- schema fields such as `title`, `severity_hint`, `expected_behavior`, and `failure_signals` map into `metadata`

A future scanner phase can add a new scan mode or selection policy that calls `packages.prompt_library.select_test_cases()` and then converts selected cases to scanner tests. That future work should add authorization, rate limits, spend controls, and target verification before any customer-facing use.

Phase 9 API placeholder routes do not run prompt-library cases. Phase 19 PDF export does not execute prompt-library cases; it only consumes Phase 18 report objects after findings are reviewed and evidence is redacted. Future API and worker integration should keep prompt selection behind authenticated, authorized, verified, and rate-limited workflows.

## Phase 7 Evaluator Usage

Phase 7 consumes raw target observations together with prompt-library metadata when that metadata is present. In particular:

- `expected_behavior` tells the evaluator or human reviewer what safe behavior looks like.
- `failure_signals` gives candidate signals to inspect in model output, tool traces, retrieval traces, or rendered output.
- `severity_hint` is only a hint. Final severity must follow `docs/methodology.md` and must be based on observed impact and evidence.
- `requires_context` and `context_setup` tell future test harnesses which synthetic fixtures are needed.

Phase 7 does not create findings from prompt IDs alone. Evaluation results require observed response evidence, severity/confidence reasoning, and redaction notes. Customer-facing findings require Phase 8 manual review and future report generation phases if automated generation is later added.

## Phase 8 Manual Audit Usage

Phase 8 uses the prompt library as a reviewed scenario source for authorized manual and semi-automated audits. Auditors can select cases by category and target type, then use the case metadata to plan safe testing, expected behavior review, failure-signal review, finding review, and retesting.

The prompt library still does not execute tests by itself, decide vulnerability status, generate reports, run public scans, or authorize target testing. Final customer-facing findings require the Phase 8 manual workflow in `docs/audits`.

## Adding New Test Cases

When adding a case:

1. Choose the existing methodology category or defer the case to a future category.
2. Add a stable ID with the category prefix.
3. Use fake/demo data only.
4. Keep the test safe and bounded.
5. Add expected safe behavior and concrete failure signals.
6. Mark context requirements clearly.
7. Update the category `expected_count` in `manifest.json`.
8. Run `python3 -m packages.prompt_library.validate`.
9. Do not add evaluator logic, API routes, dashboard UI, database persistence, report generation, or public scan execution as part of prompt-library changes.

## Safety Boundaries

The prompt library must not include:

- real API keys, passwords, private keys, tokens, or secrets
- real customer records, personal data, or proprietary documents
- instructions to hack real systems
- destructive tool actions against real targets
- malware, phishing, evasion, credential theft, or unsafe exploit automation
- browser automation or public scan execution

Tool/function abuse tests use mock actions only. RAG leakage tests use fake canaries and fictional document names only. Unsafe output tests use escaped and sanitized examples.

## Versioning Rules

- Library version is stored in `manifest.json`.
- Test-case versions should change when the input, expected behavior, failure signals, target types, or safety assumptions change.
- Prompt changes can affect findings and retest interpretation, so changes should be reviewable and traceable.
- Evaluator versions should remain separate from prompt-library versions.
