from __future__ import annotations

import unittest
from os import environ

from app.auth import (
    AuthUnavailableError,
    AuthenticationRequiredError,
    build_auth_configuration_status,
    extract_bearer_token,
    require_current_user,
)
from app.config import Settings, get_settings
from app.errors import NotImplementedApiError
from app.main import create_app
from app.routes.auth import auth_status
from app.routes.health import health_check
from app.routes.projects import projects_placeholder
from app.routes.targets import targets_placeholder
from app.routes.scans import scans_placeholder
from app.routes.verification import verification_placeholder
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
            "AUTH_ENABLED": environ.get("AUTH_ENABLED"),
            "SHERLOCK_AUTH_ENABLED": environ.get("SHERLOCK_AUTH_ENABLED"),
            "SUPABASE_URL": environ.get("SUPABASE_URL"),
            "SUPABASE_ANON_KEY": environ.get("SUPABASE_ANON_KEY"),
            "SUPABASE_SERVICE_ROLE_KEY": environ.get("SUPABASE_SERVICE_ROLE_KEY"),
            "SUPABASE_JWKS_URL": environ.get("SUPABASE_JWKS_URL"),
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
                "SHERLOCK_CURRENT_PHASE": "Phase 15 Queue + Worker System completed",
                "DATABASE_URL": "",
                "AUTH_ENABLED": "false",
                "SHERLOCK_AUTH_ENABLED": "false",
                "SUPABASE_URL": "",
                "SUPABASE_ANON_KEY": "",
                "SUPABASE_SERVICE_ROLE_KEY": "",
                "SUPABASE_JWKS_URL": "",
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
        self.assertEqual(settings.current_phase, "Phase 15 Queue + Worker System completed")
        self.assertEqual(settings.database_url, "")
        self.assertEqual(settings.supabase_url, "")
        self.assertEqual(settings.supabase_anon_key, "")
        self.assertEqual(settings.supabase_service_role_key, "")
        self.assertEqual(settings.supabase_jwks_url, "")
        self.assertFalse(settings.public_scanning_enabled)
        self.assertFalse(settings.database_enabled)
        self.assertFalse(settings.authentication_enabled)
        self.assertFalse(settings.supabase_project_configured)
        self.assertFalse(settings.supabase_jwks_url_configured)
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
        self.assertEqual(response.data["security_boundaries"]["auth_provider"], "supabase")
        self.assertFalse(response.data["security_boundaries"]["auth_token_validation_active"])
        self.assertFalse(response.data["security_boundaries"]["public_scanning_enabled"])
        module_names = {module["module"] for module in response.data["modules"]}
        self.assertIn("auth", module_names)
        self.assertIn("projects", module_names)
        self.assertIn("scans", module_names)
        self.assertIn("verification", module_names)

    def test_auth_status_documents_safe_defaults(self) -> None:
        response = auth_status()
        self.assertTrue(response.success)
        self.assertEqual(response.data["provider"], "supabase")
        self.assertFalse(response.data["authentication_enabled"])
        self.assertFalse(response.data["supabase_project_configured"])
        self.assertFalse(response.data["jwt_verification_configured"])
        self.assertFalse(response.data["token_validation_active"])
        self.assertFalse(response.data["production_ready"])
        self.assertIn("/api/v0/me", response.data["protected_endpoints"])

    def test_auth_configuration_treats_placeholders_as_not_configured(self) -> None:
        settings = Settings(
            authentication_enabled=True,
            supabase_url="replace-with-supabase-url",
            supabase_anon_key="replace-with-supabase-anon-key",
            supabase_service_role_key="replace-with-server-only-supabase-service-role-key",
            supabase_jwks_url="replace-with-supabase-jwks-url",
        )
        status = build_auth_configuration_status(settings)
        self.assertTrue(status.authentication_enabled)
        self.assertFalse(status.supabase_project_configured)
        self.assertFalse(status.jwt_verification_configured)
        self.assertFalse(status.production_ready)

    def test_bearer_token_extraction_is_strict(self) -> None:
        self.assertEqual(extract_bearer_token("Bearer test-token"), "test-token")
        with self.assertRaises(AuthenticationRequiredError):
            extract_bearer_token(None)
        with self.assertRaises(AuthenticationRequiredError):
            extract_bearer_token("Basic test-token")

    def test_current_user_dependency_does_not_fake_auth(self) -> None:
        with self.assertRaises(AuthUnavailableError) as context:
            require_current_user(authorization="Bearer test-token")
        self.assertEqual(context.exception.status_code, 503)
        self.assertEqual(context.exception.code, "auth_unavailable")

    def test_placeholder_routes_are_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedApiError) as context:
            projects_placeholder()
        self.assertEqual(context.exception.status_code, 501)
        self.assertEqual(context.exception.code, "not_implemented")
        self.assertEqual(context.exception.details["setup_contract"]["current_behavior"], "No route persists project records; dashboard setup UI remains static/mock.")
        self.assertIn("api_keys", context.exception.details["setup_contract"]["forbidden_fields"])

    def test_target_placeholder_documents_secret_and_scan_boundaries(self) -> None:
        with self.assertRaises(NotImplementedApiError) as context:
            targets_placeholder()
        self.assertEqual(context.exception.status_code, 501)
        self.assertEqual(context.exception.code, "not_implemented")
        self.assertIn("secret storage", context.exception.details["disabled_capabilities"])
        self.assertIn("tool_using_agent", context.exception.details["setup_contract"]["ui_target_types"])
        self.assertIn("plaintext_api_key", context.exception.details["setup_contract"]["forbidden_fields"])

    def test_verification_placeholder_returns_phase14_contract(self) -> None:
        with self.assertRaises(NotImplementedApiError) as context:
            verification_placeholder()
        self.assertEqual(context.exception.status_code, 501)
        self.assertEqual(context.exception.code, "not_implemented")
        details = context.exception.details
        self.assertEqual(details["status"], "contract_placeholder")
        self.assertIn("verification_contract", details)
        contract = details["verification_contract"]
        method_names = [m["method"] for m in contract["methods"]["methods"]]
        self.assertIn("dns_txt", method_names)
        self.assertIn("html_meta_tag", method_names)
        self.assertIn("well_known_file", method_names)
        self.assertIn("manual_authorization", method_names)
        self.assertIn("chatbot_api_challenge", method_names)
        status_names = [s["status"] for s in contract["statuses"]["statuses"]]
        self.assertIn("unverified", status_names)
        self.assertIn("pending", status_names)
        self.assertIn("verified", status_names)
        self.assertIn("manual_review_required", status_names)
        self.assertTrue(contract["challenge_token_design"]["format"].startswith("sherlock_"))

    def test_scans_placeholder_returns_queue_contract(self) -> None:
        with self.assertRaises(NotImplementedApiError) as context:
            scans_placeholder()
        self.assertEqual(context.exception.status_code, 501)
        self.assertEqual(context.exception.code, "not_implemented")
        details = context.exception.details
        self.assertEqual(details["status"], "queue_foundation")
        self.assertIn("queue_contract", details)
        contract = details["queue_contract"]
        job_types = [jt["job_type"] for jt in contract["job_types"]]
        self.assertIn("scan.run", job_types)
        self.assertIn("scan.evaluate", job_types)
        states = [s["status"] for s in contract["job_lifecycle_states"]]
        self.assertIn("queued", states)
        self.assertIn("blocked_unverified", states)
        self.assertIn("target_verified", contract["safety_gates"])
        self.assertIn("api_key", contract["forbidden_payload_fields"])

    def test_app_factory_registers_routes(self) -> None:
        app = create_app(Settings(allowed_origins=()))
        paths = {route.path for route in app.routes}
        self.assertIn("/health", paths)
        self.assertIn("/version", paths)
        self.assertIn("/api/v0/auth/status", paths)
        self.assertIn("/api/v0/me", paths)
        self.assertIn("/api/v0/projects", paths)
        self.assertIn("/api/v0/scans", paths)
        self.assertIn("/api/v0/verification", paths)


if __name__ == "__main__":
    unittest.main()
