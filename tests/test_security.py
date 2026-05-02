import pytest

from app import create_app
from config import DevelopmentConfig, ProductionConfig, TestingConfig


def test_security_headers_present(client):
    """Common browser hardening headers are added to responses."""
    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in response.headers
    assert "script-src 'self'" in response.headers["Content-Security-Policy"]
    assert "unsafe-inline" not in response.headers["Content-Security-Policy"]


def test_production_requires_strong_secret_key():
    """Production config refuses weak Flask secrets."""

    class WeakProductionConfig(ProductionConfig):
        SECRET_KEY = "short"
        RATELIMIT_STORAGE_URI = "memory://"

    with pytest.raises(ValueError, match="SECRET_KEY"):
        create_app(WeakProductionConfig)


def test_production_adds_hsts_for_secure_cookies():
    """Production responses include HSTS when secure cookies are enabled."""

    class SecureProductionConfig(ProductionConfig):
        SECRET_KEY = "x" * 32
        RATELIMIT_STORAGE_URI = "memory://"

    app = create_app(SecureProductionConfig)

    response = app.test_client().get("/")

    assert response.headers["Strict-Transport-Security"] == (
        "max-age=31536000; includeSubDomains"
    )


def test_testing_config_keeps_csrf_disabled():
    """Tests can post forms without CSRF tokens."""
    app = create_app(TestingConfig)

    assert app.config["WTF_CSRF_ENABLED"] is False


def test_development_uses_fallback_secret_for_empty_env(monkeypatch):
    """Development remains runnable when local .env leaves SECRET_KEY empty."""
    monkeypatch.setenv("SECRET_KEY", "")

    class EmptySecretDevelopmentConfig(DevelopmentConfig):
        SECRET_KEY = ""

    app = create_app(EmptySecretDevelopmentConfig)

    assert app.config["SECRET_KEY"] == "dev-key-change-in-production"


def test_development_uses_memory_rate_limit_storage(monkeypatch):
    """Development does not require Redis even if the shell exports it."""
    monkeypatch.setenv("RATELIMIT_STORAGE_URI", "redis://localhost:6379/0")

    app = create_app(DevelopmentConfig)

    assert app.config["RATELIMIT_STORAGE_URI"] == "memory://"
