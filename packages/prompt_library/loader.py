from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

PROMPT_LIBRARY_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = PROMPT_LIBRARY_ROOT / "manifest.json"
REQUIRED_TEST_CASE_FIELDS = (
    "id",
    "version",
    "category",
    "title",
    "description",
    "input",
    "tags",
    "severity_hint",
    "expected_behavior",
    "failure_signals",
    "safety_notes",
    "requires_context",
    "context_setup",
    "target_types",
    "status",
    "enabled",
    "references",
)


@dataclass(frozen=True)
class PromptTestCase:
    id: str
    version: str
    category: str
    title: str
    description: str
    input: str
    tags: List[str]
    severity_hint: str
    expected_behavior: str
    failure_signals: List[str]
    safety_notes: str
    requires_context: bool
    context_setup: Optional[Dict[str, Any]]
    target_types: List[str]
    status: str
    enabled: bool
    references: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "PromptTestCase":
        missing = [field_name for field_name in REQUIRED_TEST_CASE_FIELDS if field_name not in value]
        if missing:
            raise ValueError(f"test case is missing required fields: {', '.join(missing)}")
        return cls(
            id=_required_string(value, "id"),
            version=_required_string(value, "version"),
            category=_required_string(value, "category"),
            title=_required_string(value, "title"),
            description=_required_string(value, "description"),
            input=_required_string(value, "input"),
            tags=_required_string_list(value, "tags"),
            severity_hint=_required_string(value, "severity_hint"),
            expected_behavior=_required_string(value, "expected_behavior"),
            failure_signals=_required_string_list(value, "failure_signals"),
            safety_notes=_required_string(value, "safety_notes"),
            requires_context=_required_bool(value, "requires_context"),
            context_setup=_optional_dict(value, "context_setup"),
            target_types=_required_string_list(value, "target_types"),
            status=_required_string(value, "status"),
            enabled=_required_bool(value, "enabled"),
            references=_required_string_list(value, "references"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "input": self.input,
            "tags": list(self.tags),
            "severity_hint": self.severity_hint,
            "expected_behavior": self.expected_behavior,
            "failure_signals": list(self.failure_signals),
            "safety_notes": self.safety_notes,
            "requires_context": self.requires_context,
            "context_setup": self.context_setup,
            "target_types": list(self.target_types),
            "status": self.status,
            "enabled": self.enabled,
            "references": list(self.references),
        }

    def to_scanner_test(self) -> Any:
        from packages.scanner_engine.models import ScannerTest

        return ScannerTest(
            test_id=self.id,
            category=self.category,
            input=self.input,
            metadata={
                "prompt_library": "powerdetect-sherlock-attack-prompt-library",
                "prompt_version": self.version,
                "title": self.title,
                "description": self.description,
                "tags": list(self.tags),
                "severity_hint": self.severity_hint,
                "expected_behavior": self.expected_behavior,
                "failure_signals": list(self.failure_signals),
                "safety_notes": self.safety_notes,
                "requires_context": self.requires_context,
                "context_setup": self.context_setup,
                "target_types": list(self.target_types),
                "status": self.status,
                "references": list(self.references),
                "evaluation_status": "not_evaluated_by_prompt_library",
            },
        )


@dataclass(frozen=True)
class PromptLibrary:
    manifest: Dict[str, Any]
    test_cases: List[PromptTestCase]

    def enabled_cases(self) -> List[PromptTestCase]:
        return [test_case for test_case in self.test_cases if test_case.enabled and test_case.status == "enabled"]

    def by_category(self, category: str) -> List[PromptTestCase]:
        return [test_case for test_case in self.test_cases if test_case.category == category]

    def to_scanner_tests(self, max_tests: Optional[int] = None) -> List[Any]:
        cases = self.enabled_cases()
        if max_tests is not None:
            cases = cases[:max_tests]
        return [test_case.to_scanner_test() for test_case in cases]


def load_prompt_library(root: Path | str = PROMPT_LIBRARY_ROOT) -> PromptLibrary:
    root_path = Path(root)
    manifest_path = root_path / "manifest.json"
    manifest = _load_json_object(manifest_path)
    test_cases: List[PromptTestCase] = []
    for category_entry in manifest.get("categories", []):
        category_file = category_entry.get("file")
        if not isinstance(category_file, str) or not category_file:
            raise ValueError("manifest category file must be a non-empty string")
        category_payload = _load_json_object(root_path / category_file)
        category_name = _required_string(category_payload, "category")
        for raw_case in category_payload.get("test_cases", []):
            if not isinstance(raw_case, dict):
                raise ValueError(f"test case in {category_file} must be an object")
            test_case = PromptTestCase.from_dict(raw_case)
            if test_case.category != category_name:
                raise ValueError(f"{test_case.id} category does not match file category {category_name}")
            test_cases.append(test_case)
    return PromptLibrary(manifest=manifest, test_cases=test_cases)


def validate_prompt_library(root: Path | str = PROMPT_LIBRARY_ROOT) -> List[str]:
    library = load_prompt_library(root)
    errors: List[str] = []
    allowed = library.manifest.get("allowed_values", {})
    allowed_severities = set(allowed.get("severity_hint", []))
    allowed_statuses = set(allowed.get("status", []))
    allowed_target_types = set(allowed.get("target_types", []))
    seen_ids: set[str] = set()
    category_counts: Dict[str, int] = {}

    for test_case in library.test_cases:
        if test_case.id in seen_ids:
            errors.append(f"duplicate test case id: {test_case.id}")
        seen_ids.add(test_case.id)
        category_counts[test_case.category] = category_counts.get(test_case.category, 0) + 1
        if test_case.severity_hint not in allowed_severities:
            errors.append(f"{test_case.id} has unsupported severity_hint: {test_case.severity_hint}")
        if test_case.status not in allowed_statuses:
            errors.append(f"{test_case.id} has unsupported status: {test_case.status}")
        unknown_targets = [target_type for target_type in test_case.target_types if target_type not in allowed_target_types]
        if unknown_targets:
            errors.append(f"{test_case.id} has unsupported target_types: {', '.join(unknown_targets)}")
        if test_case.requires_context and test_case.context_setup is None:
            errors.append(f"{test_case.id} requires_context but has no context_setup")
        if not test_case.requires_context and test_case.context_setup is not None:
            errors.append(f"{test_case.id} has context_setup but requires_context is false")
        if test_case.status == "enabled" and not test_case.enabled:
            errors.append(f"{test_case.id} status is enabled but enabled is false")

    for category_entry in library.manifest.get("categories", []):
        category_id = category_entry.get("id")
        expected_count = category_entry.get("expected_count")
        if isinstance(category_id, str) and isinstance(expected_count, int):
            actual_count = category_counts.get(category_id, 0)
            if actual_count != expected_count:
                errors.append(f"{category_id} expected {expected_count} test cases but found {actual_count}")
    return errors


def iter_enabled_test_cases(root: Path | str = PROMPT_LIBRARY_ROOT) -> Iterable[PromptTestCase]:
    return iter(load_prompt_library(root).enabled_cases())


def _load_json_object(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _required_string(value: Dict[str, Any], field_name: str) -> str:
    field_value = value.get(field_name)
    if not isinstance(field_value, str) or not field_value:
        raise ValueError(f"{field_name} must be a non-empty string")
    return field_value


def _required_string_list(value: Dict[str, Any], field_name: str) -> List[str]:
    field_value = value.get(field_name)
    if not isinstance(field_value, list) or not field_value:
        raise ValueError(f"{field_name} must be a non-empty list")
    if any(not isinstance(item, str) or not item for item in field_value):
        raise ValueError(f"{field_name} must contain only non-empty strings")
    return list(field_value)


def _required_bool(value: Dict[str, Any], field_name: str) -> bool:
    field_value = value.get(field_name)
    if not isinstance(field_value, bool):
        raise ValueError(f"{field_name} must be a boolean")
    return field_value


def _optional_dict(value: Dict[str, Any], field_name: str) -> Optional[Dict[str, Any]]:
    field_value = value.get(field_name)
    if field_value is None:
        return None
    if not isinstance(field_value, dict):
        raise ValueError(f"{field_name} must be an object or null")
    return dict(field_value)


def select_test_cases(
    categories: Optional[Sequence[str]] = None,
    target_types: Optional[Sequence[str]] = None,
    include_experimental: bool = False,
    max_tests: Optional[int] = None,
    root: Path | str = PROMPT_LIBRARY_ROOT,
) -> List[PromptTestCase]:
    library = load_prompt_library(root)
    selected = []
    category_filter = set(categories or [])
    target_type_filter = set(target_types or [])
    for test_case in library.test_cases:
        if not test_case.enabled:
            continue
        if test_case.status == "experimental" and not include_experimental:
            continue
        if test_case.status == "disabled":
            continue
        if category_filter and test_case.category not in category_filter:
            continue
        if target_type_filter and not target_type_filter.intersection(test_case.target_types):
            continue
        selected.append(test_case)
    if max_tests is not None:
        selected = selected[:max_tests]
    return selected
