from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any, Dict

from .config import SENSITIVE_HEADER_NAMES, ScanConfig, TargetConfig
from .models import ScannerTest, TargetResponse


class TargetAdapter(ABC):
    def __init__(self, target_config: TargetConfig, timeout_seconds: int) -> None:
        self.target_config = target_config
        self.timeout_seconds = timeout_seconds

    @abstractmethod
    def send(self, test: ScannerTest) -> TargetResponse:
        raise NotImplementedError


class MockTargetAdapter(TargetAdapter):
    def send(self, test: ScannerTest) -> TargetResponse:
        body = {
            "message": f"Mock response for {test.test_id}",
            "received_input": test.input,
            "internal_only": True,
        }
        return TargetResponse(
            status_code=200,
            body=json.dumps(body, indent=2),
            metadata={
                "adapter": "mock",
                "network_used": False,
            },
        )


class HttpApiTargetAdapter(TargetAdapter):
    def send(self, test: ScannerTest) -> TargetResponse:
        if not self.target_config.endpoint_url:
            raise ValueError("endpoint_url is required for http_api target adapter")
        request = self._build_request(test)
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_body = response.read().decode("utf-8", errors="replace")
                duration_ms = int((time.perf_counter() - started) * 1000)
                return TargetResponse(
                    status_code=response.status,
                    body=response_body,
                    metadata={
                        "adapter": "http_api",
                        "headers": _redact_headers(dict(response.headers.items())),
                        "duration_ms": duration_ms,
                    },
                )
        except urllib.error.HTTPError as error:
            response_body = error.read().decode("utf-8", errors="replace")
            return TargetResponse(
                status_code=error.code,
                body=response_body,
                metadata={
                    "adapter": "http_api",
                    "http_error": True,
                    "reason": str(error.reason),
                },
            )

    def _build_request(self, test: ScannerTest) -> urllib.request.Request:
        method = self.target_config.method
        headers = dict(self.target_config.headers)
        body = self._build_body(test)
        data = None
        if method in ("POST", "PUT", "PATCH"):
            data = json.dumps(body).encode("utf-8")
            headers.setdefault("Content-Type", "application/json")
        elif body:
            headers.setdefault("X-Sherlock-Test-Input", test.input)
        return urllib.request.Request(
            self.target_config.endpoint_url,
            data=data,
            headers=headers,
            method=method,
        )

    def _build_body(self, test: ScannerTest) -> Dict[str, Any]:
        body = dict(self.target_config.body_mapping.static_body)
        body[self.target_config.body_mapping.message_field] = test.input
        return body


def build_target_adapter(scan_config: ScanConfig) -> TargetAdapter:
    if scan_config.target.type == "mock":
        return MockTargetAdapter(scan_config.target, scan_config.timeout_seconds)
    if scan_config.target.type == "http_api":
        return HttpApiTargetAdapter(scan_config.target, scan_config.timeout_seconds)
    raise ValueError(f"Unsupported target type: {scan_config.target.type}")


def _redact_headers(headers: Dict[str, str]) -> Dict[str, str]:
    return {
        key: "[REDACTED]" if key.strip().lower() in SENSITIVE_HEADER_NAMES else value
        for key, value in headers.items()
    }
