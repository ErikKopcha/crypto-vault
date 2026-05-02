from flask import Flask

from app.extensions import csrf, limiter
from config import validate_secret_key


def create_app(config_class=None):
    """
    Create and configure the Flask application.

    @param config_class - Config class (e.g. DevelopmentConfig). If None, no config.
    @raises ValueError - In production, if SECRET_KEY is not set
    """
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)

        if (
            not app.config.get("TESTING")
            and not app.config.get("REQUIRE_STRONG_SECRET_KEY")
            and not app.config.get("SECRET_KEY")
        ):
            app.config["SECRET_KEY"] = "dev-key-change-in-production"

        if app.config.get("REQUIRE_STRONG_SECRET_KEY"):
            validate_secret_key(app.config.get("SECRET_KEY", ""))

        if (
            app.config.get("REQUIRE_PERSISTENT_RATE_LIMIT_STORAGE")
            and not app.config.get("RATELIMIT_STORAGE_URI")
        ):
            raise ValueError(
                "RATELIMIT_STORAGE_URI must be set in production "
                "(for example, redis://localhost:6379/0)"
            )

    csrf.init_app(app)
    limiter.init_app(app)
    _register_security_headers(app)

    # Register blueprints
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app


def _register_security_headers(app: Flask) -> None:
    """Add security headers to all responses."""

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
        )
        if app.config.get("SESSION_COOKIE_SECURE"):
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self'"
        )
        return response
