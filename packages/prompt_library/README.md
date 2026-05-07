# Attack Prompt Library V0

Status: Phase 6 internal foundation. Phase 7 evaluator system and Phase 8 manual audit workflow are available separately.

This package contains the first internal PowerDetect Sherlock attack/test prompt library. It is a versioned, reviewable library of safe AI security test cases mapped to the Phase 3 methodology categories.

## What Phase 6 Adds

- versioned prompt library manifest
- JSON schema reference for test cases
- category-based JSON test-case files
- safe metadata for expected behavior and `failure_signals`: observable signals an evaluator or reviewer can inspect
- stdlib-only loader and validator utilities
- conversion helper for the Phase 5 `ScannerTest` shape

## What Is Not Implemented Here

- evaluator logic
- LLM-as-judge behavior
- vulnerability detection
- real severity scoring
- backend scan APIs
- dashboard integration
- authentication
- database persistence
- billing
- queue workers
- report generation
- PDF export
- public scan execution
- admin panel
- target ownership verification
- SSRF protection
- browser automation
- unsafe exploit automation

## Package Structure

```text
packages/prompt_library/
|-- __init__.py
|-- loader.py
|-- validate.py
|-- manifest.json
|-- schema/
|   `-- test-case.schema.json
|-- categories/
|   |-- prompt_injection.json
|   |-- system_prompt_leakage.json
|   |-- sensitive_data_leakage.json
|   |-- rag_data_leakage.json
|   |-- indirect_prompt_injection.json
|   |-- tool_function_abuse.json
|   |-- unsafe_output_handling.json
|   `-- cost_abuse.json
`-- README.md
```

## Validate Locally

From the repository root:

```bash
python3 -m packages.prompt_library.validate
```

The validator checks JSON parseability, required fields, duplicate IDs, category counts, supported `severity_hint`: non-binding evaluator/reporting hint types, and context setup consistency.

## Loader Usage

```python
from packages.prompt_library import load_prompt_library, select_test_cases

library = load_prompt_library()
enabled_cases = library.enabled_cases()
rag_cases = select_test_cases(categories=["rag_data_leakage"], target_types=["rag"])
scanner_tests = library.to_scanner_tests(max_tests=5)
```

The scanner conversion returns Phase 5 `ScannerTest` objects with prompt-library metadata attached. The Phase 5 scanner runner does not execute this library by default.

Phase 8 manual audits can use selected prompt-library cases as reviewed scenario inputs, but final findings still require human review under `../../docs/audits`.

## Safety Rules

- Use fake/demo data only.
- Do not add real secrets, real credentials, real customer data, or production tokens.
- Keep tool/function abuse cases mock-only and side-effect-free.
- Keep RAG canaries fake and clearly labeled.
- Keep unsafe output examples sanitized, escaped, and safe for development.
- Do not add exploit automation, browser automation, evaluator logic, or public scan execution here.
