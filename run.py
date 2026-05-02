"""
Run the Flask application.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent / ".env")


def _create_configured_app():
    """Create the Flask app after loading environment variables."""
    from app import create_app
    from config import config

    env = os.environ.get("FLASK_ENV", "default")
    return create_app(config[env])


app = _create_configured_app()

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port)
