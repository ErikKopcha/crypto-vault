import pytest

from app import create_app
from config import TestingConfig


@pytest.fixture
def app():
    """Create application for testing."""
    return create_app(TestingConfig)


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()
