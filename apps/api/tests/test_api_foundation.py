from __future__ import annotations

import unittest
from os import environ

from app.config import Settings, get_settings
from app.errors import NotImplementedApiError
from app.main import create_app
from app.routes.health import health_check
from app.routes.projects import projects_placeholder
from app.routes.version import version_status


class ApiFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._saved_environment = {
            "SHERLOCK_APP_NAME": environ.get("SHERLOCK_APP_NAME"),
            "SHERLOCK_BRAND": environ.get("SHERLOCK_BRAND"),
            "SHERLOCK_MARKETING_NAME": environ.get("SHERLOCK_MARKETING_NAME"),
            "SHERLOCK_ENVIRONMENT": environ.get("SHERLOCK_ENVIRONMENT"),
            "SHERLOCK_API_VERSION": environ.get("SHERLOCK_API_VERSION"),
            "SHERLOCK_CURRENT_PHASE": environ.get("SHERLOCK_CURRENT_PHASE"),
            "DATABASE_URL": environ.get("DATABASE_URL"),
            "SHERLOCK_DEBUG": environ.get("SHERLOCK_DEBUG"),
            "SHERLOCK_ALLOWED_ORIGINS": environ.get("SHERLOCK_ALLOWED_ORIGINS"),
        }
        environ.update(
            {
                "SHERLOCK_APP_NAME": "Sherlock",
                "SHERLOCK_BRAND": "PowerDetect",
                "SHERLOCK_MARKETING_NAME": "PowerDetect Sherlock",
                "SHERLOCK_ENVIRONMENT": "local",
                "SHERLOCK_API_VERSION": "v0",
                "SHERLOCK_CURRENT_PHASE": "Phase 10 Database Setup completed",
                "DATABASE_URL": "",
                "SHERLOCK_DEBUG": "false",
                "SHERLOCK_ALLOWED_ORIGINS": "http://localhost:3000,http://localhost:4173",
            }
        )
        get_settings.cache_clear()

    def tearDown(self) -> None:
        for key, value in self._saved_environment.items():
            if value is None:
                environ.pop(key, None)
            else:
                environ[key] = value
        get_settings.cache_clear()

    def test_settings_defaults_are_safe(self) -> None:
        settings = Settings()
        self.assertEqual(settings.app_name, "Sherlock")
        self.assertEqual(settings.brand_name, "PowerDetect")
        self.assertEqual(settings.marketing_name, "PowerDetect Sherlock")
        self.assertEqual(settings.api_version, "v0")
        self.assertEqual(settings.database_url, "")
        self.assertFalse(settings.public_scanning_enabled)
        self.assertFalse(settings.database_enabled)
        self.assertFalse(settings.authentication_enabled)
        self.assertFalse(settings.billing_enabled)
        self.assertFalse(settings.worker_enabled)

    def test_health_response_shape(self) -> None:
        response = health_check()
        self.assertTrue(response.success)
        self.assertIsNone(response.error)
        self.assertEqual(response.data["app_name"], "Sherlock")
        self.assertEqual(response.data["brand_name"], "PowerDetect")
        self.assertEqual(response.data["status"], "ok")
        self.assertFalse(response.data["public_scanning_enabled"])
        self.assertIn("api_version", response.metadata)

    def test_version_response_documents_boundaries(self) -> None:
        response = version_status()
        self.assertTrue(response.success)
        self.assertFalse(response.data["security_boundaries"]["database_enabled"])
        self.assertFalse(response.data["security_boundaries"]["authentication_enabled"])
        self.assertFalse(response.data["security_boundaries"]["public_scanning_enabled"])
        module_names = {module["module"] for module in response.data["modules"]}
        self.assertIn("projects", module_names)
        self.assertIn("scans", module_names)
        self.assertIn("verification", module_names)

    def test_placeholder_routes_are_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedApiError) as context:
            projects_placeholder()
        self.assertEqual(context.exception.status_code, 501)
        self.assertEqual(context.exception.code, "not_implemented")

    def test_app_factory_registers_routes(self) -> None:
        app = create_app(Settings(allowed_origins=()))
        paths = {route.path for route in app.routes}
        self.assertIn("/health", paths)
        self.assertIn("/version", paths)
        self.assertIn("/api/v0/projects", paths)
        self.assertIn("/api/v0/scans", paths)
        self.assertIn("/api/v0/verification", paths)


if __name__ == "__main__":
    unittest.main()
