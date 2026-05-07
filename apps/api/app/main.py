from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .errors import register_error_handlers
from .logging import configure_logging
from .routes import findings, health, projects, reports, scans, targets, verification, version


def create_app(settings: Settings | None = None) -> FastAPI:
    active_settings = settings or get_settings()
    configure_logging(active_settings.debug)

    app = FastAPI(
        title=f"{active_settings.marketing_name} API",
        version=active_settings.api_version,
        description="Phase 10 database foundation for Sherlock. Public scanning, auth, active API persistence, billing, and workers are not implemented.",
        debug=active_settings.debug,
    )

    if active_settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(active_settings.allowed_origins),
            allow_credentials=False,
            allow_methods=["GET"],
            allow_headers=["*"],
        )

    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(version.router)

    api_prefix = active_settings.api_prefix
    app.include_router(projects.router, prefix=api_prefix)
    app.include_router(targets.router, prefix=api_prefix)
    app.include_router(scans.router, prefix=api_prefix)
    app.include_router(findings.router, prefix=api_prefix)
    app.include_router(reports.router, prefix=api_prefix)
    app.include_router(verification.router, prefix=api_prefix)

    return app


app = create_app()
