"""
Configuration settings for the application.
"""

import os
import secrets


# Path constants
DEFAULT_ENCRYPTED_FOLDER = "encrypted"

# PBKDF2 iteration bounds (security vs DoS prevention)
MIN_ITERATIONS = 100_000
MAX_ITERATIONS = 2_000_000
DEFAULT_ITERATIONS = 600_000
MIN_SECRET_KEY_BYTES = 32

# File upload limit (10 MB)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# Input length limits (DoS prevention)
MAX_DATA_LENGTH = 1024 * 1024  # 1 MB for plaintext/encrypted JSON
MAX_PASSWORD_LENGTH = 256


class Config:
    """Base configuration."""

    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    REQUIRE_STRONG_SECRET_KEY = False
    REQUIRE_PERSISTENT_RATE_LIMIT_STORAGE = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"
    RATELIMIT_STORAGE_URI = "memory://"


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True
    SECRET_KEY = "test-secret-key"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    RATELIMIT_STORAGE_URI = "memory://"


class ProductionConfig(Config):
    """Production configuration — SECRET_KEY required."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    REQUIRE_STRONG_SECRET_KEY = True
    REQUIRE_PERSISTENT_RATE_LIMIT_STORAGE = True
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI")


def validate_secret_key(secret_key: str) -> None:
    """
    Validate Flask secret entropy for signed session and CSRF protection.

    @param secret_key - Flask SECRET_KEY value.
    @raises ValueError - If the secret is absent or too weak.
    """
    if not secret_key:
        raise ValueError("SECRET_KEY environment variable must be set in production")

    if len(secret_key.encode("utf-8")) < MIN_SECRET_KEY_BYTES:
        raise ValueError(
            f"SECRET_KEY must be at least {MIN_SECRET_KEY_BYTES} bytes"
        )

    weak_values = {"dev-key-change-in-production", "test-secret-key"}
    if secret_key in weak_values or secrets.compare_digest(secret_key, "changeme"):
        raise ValueError("SECRET_KEY must be a strong random value")


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
