"""
Configuration settings for the application.
"""

import os


# Path constants
DEFAULT_ENCRYPTED_FOLDER = "encrypted"

# PBKDF2 iteration bounds (security vs DoS prevention)
MIN_ITERATIONS = 1_000
MAX_ITERATIONS = 1_000_000
DEFAULT_ITERATIONS = 100_000

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


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True
    SECRET_KEY = "test-secret-key"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production configuration — SECRET_KEY required."""

    SECRET_KEY = os.environ.get("SECRET_KEY")


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
