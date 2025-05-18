"""
Flask application initialization.
"""

from flask import Flask

def create_app(config=None):
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    app.secret_key = "development-key"  # Change this in production
    
    # Load configuration
    if config:
        app.config.from_object(config)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app 