from flask import Flask


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

    # Register blueprints
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app
