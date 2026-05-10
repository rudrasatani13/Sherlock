from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Tuple


def _read_env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value is not None:
            return value
    return default


def _has_config_value(value: str) -> bool:
    normalized = value.strip().strip('"').strip("'")
    if not normalized:
        return False
    lowered = normalized.lower()
    if lowered.startswith(("replace-with-", "placeholder", "your-", "example-")):
        return False
    return lowered not in {"changeme", "change-me", "not-configured", "none", "null"}


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_origins(value: str | None) -> Tuple[str, ...]:
    if value is None:
        return ("http://localhost:3000", "http://localhost:4173")
    return tuple(origin.strip() for origin in value.split(",") if origin.strip())


@dataclass(frozen=True)
class Settings:
    app_name: str = field(default_factory=lambda: os.getenv("SHERLOCK_APP_NAME", "Sherlock"))
    brand_name: str = field(default_factory=lambda: os.getenv("SHERLOCK_BRAND", "PowerDetect"))
    marketing_name: str = field(default_factory=lambda: os.getenv("SHERLOCK_MARKETING_NAME", "PowerDetect Sherlock"))
    environment: str = field(default_factory=lambda: os.getenv("SHERLOCK_ENVIRONMENT", "local"))
    api_version: str = field(default_factory=lambda: os.getenv("SHERLOCK_API_VERSION", "v0"))
    current_phase: str = field(
        default_factory=lambda: os.getenv("SHERLOCK_CURRENT_PHASE", "Phase 18 Web Report foundation completed")
    )
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    supabase_url: str = field(default_factory=lambda: os.getenv("SUPABASE_URL", ""))
    supabase_anon_key: str = field(default_factory=lambda: os.getenv("SUPABASE_ANON_KEY", ""))
    supabase_service_role_key: str = field(default_factory=lambda: os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""))
    supabase_jwks_url: str = field(default_factory=lambda: os.getenv("SUPABASE_JWKS_URL", ""))
    debug: bool = field(default_factory=lambda: _parse_bool(os.getenv("SHERLOCK_DEBUG"), default=False))
    allowed_origins: Tuple[str, ...] = field(
        default_factory=lambda: _parse_origins(os.getenv("SHERLOCK_ALLOWED_ORIGINS"))
    )
    public_scanning_enabled: bool = False
    database_enabled: bool = False
    authentication_enabled: bool = field(
        default_factory=lambda: _parse_bool(_read_env("AUTH_ENABLED", "SHERLOCK_AUTH_ENABLED"), default=False)
    )
    billing_enabled: bool = False
    worker_enabled: bool = field(
        default_factory=lambda: _parse_bool(os.getenv("WORKER_ENABLED"), default=False)
    )
    queue_backend: str = field(default_factory=lambda: os.getenv("QUEUE_BACKEND", "local"))
    scan_limits_enabled: bool = field(
        default_factory=lambda: _parse_bool(os.getenv("SCAN_LIMITS_ENABLED"), default=True)
    )
    default_scan_type: str = field(
        default_factory=lambda: os.getenv("DEFAULT_SCAN_TYPE", "quick_scan")
    )
    deep_scan_enabled: bool = field(
        default_factory=lambda: _parse_bool(os.getenv("DEEP_SCAN_ENABLED"), default=False)
    )

    @property
    def api_prefix(self) -> str:
        return f"/api/{self.api_version}"

    @property
    def supabase_url_configured(self) -> bool:
        return _has_config_value(self.supabase_url)

    @property
    def supabase_anon_key_configured(self) -> bool:
        return _has_config_value(self.supabase_anon_key)

    @property
    def supabase_service_role_key_configured(self) -> bool:
        return _has_config_value(self.supabase_service_role_key)

    @property
    def supabase_jwks_url_configured(self) -> bool:
        return _has_config_value(self.supabase_jwks_url)

    @property
    def supabase_project_configured(self) -> bool:
        return self.supabase_url_configured and self.supabase_anon_key_configured


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
