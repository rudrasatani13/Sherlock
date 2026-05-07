from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


SUPPORTED_TARGET_TYPES = ("mock", "http_api")
SUPPORTED_METHODS = ("GET", "POST", "PUT", "PATCH")
SUPPORTED_SCAN_MODES = ("safe_smoke",)
DEFAULT_OUTPUT_DIR = "scan-results"
DEFAULT_TIMEOUT_SECONDS = 10
DEFAULT_MAX_TESTS = 3
SENSITIVE_HEADER_NAMES = ("authorization", "cookie", "proxy-authorization", "x-api-key")


@dataclass
class BodyMapping:
    message_field: str = "message"
    static_body: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "BodyMapping":
        if not isinstance(value, dict):
            raise ValueError("target.body_mapping must be an object")
        message_field = value.get("message_field", "message")
        static_body = value.get("static_body", {})
        if not isinstance(message_field, str) or not message_field:
            raise ValueError("target.body_mapping.message_field must be a non-empty string")
        if not isinstance(static_body, dict):
            raise ValueError("target.body_mapping.static_body must be an object")
        return cls(message_field=message_field, static_body=static_body)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_field": self.message_field,
            "static_body": self.static_body,
        }


@dataclass
class TargetConfig:
    name: str
    type: str
    endpoint_url: Optional[str] = None
    method: str = "POST"
    headers: Dict[str, str] = field(default_factory=dict)
    body_mapping: BodyMapping = field(default_factory=BodyMapping)
    notes: str = ""

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "TargetConfig":
        if not isinstance(value, dict):
            raise ValueError("target must be an object")
        name = value.get("name")
        target_type = value.get("type")
        endpoint_url = value.get("endpoint_url")
        method = value.get("method", "POST")
        headers = value.get("headers", {})
        body_mapping = BodyMapping.from_dict(value.get("body_mapping", {}))
        notes = value.get("notes", "")
        if not isinstance(name, str) or not name:
            raise ValueError("target.name must be a non-empty string")
        if target_type not in SUPPORTED_TARGET_TYPES:
            raise ValueError(f"target.type must be one of: {', '.join(SUPPORTED_TARGET_TYPES)}")
        if target_type == "http_api" and (not isinstance(endpoint_url, str) or not endpoint_url):
            raise ValueError("target.endpoint_url is required for http_api targets")
        if method.upper() not in SUPPORTED_METHODS:
            raise ValueError(f"target.method must be one of: {', '.join(SUPPORTED_METHODS)}")
        if not isinstance(headers, dict):
            raise ValueError("target.headers must be an object")
        normalized_headers = {}
        for key, header_value in headers.items():
            if not isinstance(key, str) or not isinstance(header_value, str):
                raise ValueError("target.headers keys and values must be strings")
            normalized_headers[key] = header_value
        if not isinstance(notes, str):
            raise ValueError("target.notes must be a string")
        return cls(
            name=name,
            type=target_type,
            endpoint_url=endpoint_url,
            method=method.upper(),
            headers=normalized_headers,
            body_mapping=body_mapping,
            notes=notes,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "endpoint_url": self.endpoint_url,
            "method": self.method,
            "headers": {
                key: "[REDACTED]" if key.strip().lower() in SENSITIVE_HEADER_NAMES else value
                for key, value in self.headers.items()
            },
            "body_mapping": self.body_mapping.to_dict(),
            "notes": self.notes,
        }


@dataclass
class ScanConfig:
    target: TargetConfig
    scan_mode: str = "safe_smoke"
    max_tests: int = DEFAULT_MAX_TESTS
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    output_dir: str = DEFAULT_OUTPUT_DIR
    notes: str = ""

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "ScanConfig":
        if not isinstance(value, dict):
            raise ValueError("scan config must be an object")
        target = TargetConfig.from_dict(value.get("target", {}))
        scan_mode = value.get("scan_mode", "safe_smoke")
        max_tests = value.get("max_tests", DEFAULT_MAX_TESTS)
        timeout_seconds = value.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
        output_dir = value.get("output_dir", DEFAULT_OUTPUT_DIR)
        notes = value.get("notes", "")
        if scan_mode not in SUPPORTED_SCAN_MODES:
            raise ValueError(f"scan_mode must be one of: {', '.join(SUPPORTED_SCAN_MODES)}")
        if not isinstance(max_tests, int) or max_tests < 1:
            raise ValueError("max_tests must be a positive integer")
        if max_tests > 10:
            raise ValueError("max_tests must be 10 or lower for the Phase 5 internal runner")
        if not isinstance(timeout_seconds, int) or timeout_seconds < 1:
            raise ValueError("timeout_seconds must be a positive integer")
        if timeout_seconds > 60:
            raise ValueError("timeout_seconds must be 60 or lower for the Phase 5 internal runner")
        if not isinstance(output_dir, str) or not output_dir:
            raise ValueError("output_dir must be a non-empty string")
        if not isinstance(notes, str):
            raise ValueError("notes must be a string")
        return cls(
            target=target,
            scan_mode=scan_mode,
            max_tests=max_tests,
            timeout_seconds=timeout_seconds,
            output_dir=output_dir,
            notes=notes,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target.to_dict(),
            "scan_mode": self.scan_mode,
            "max_tests": self.max_tests,
            "timeout_seconds": self.timeout_seconds,
            "output_dir": self.output_dir,
            "notes": self.notes,
        }


def load_scan_config(path: str) -> ScanConfig:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return ScanConfig.from_dict(data)
