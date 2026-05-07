from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Tuple


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
        default_factory=lambda: os.getenv("SHERLOCK_CURRENT_PHASE", "Phase 10 Database Setup completed")
    )
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    debug: bool = field(default_factory=lambda: _parse_bool(os.getenv("SHERLOCK_DEBUG"), default=False))
    allowed_origins: Tuple[str, ...] = field(
        default_factory=lambda: _parse_origins(os.getenv("SHERLOCK_ALLOWED_ORIGINS"))
    )
    public_scanning_enabled: bool = False
    database_enabled: bool = False
    authentication_enabled: bool = False
    billing_enabled: bool = False
    worker_enabled: bool = False

    @property
    def api_prefix(self) -> str:
        return f"/api/{self.api_version}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
