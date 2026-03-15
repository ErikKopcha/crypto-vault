from flask import Flask

from app.extensions import csrf, limiter


def create_app(config_class=None):
    """
    Create and configure the Flask application.

    @param config_class - Config class (e.g. DevelopmentConfig). If None, no config.
    @raises ValueError - In production, if SECRET_KEY is not set
    """
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
        # Production: require SECRET_KEY (testing has its own)
        if not app.config.get("TESTING") and not app.config.get("SECRET_KEY"):
            raise ValueError(
                "SECRET_KEY environment variable must be set in production"
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
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self'"
        )
        return response
