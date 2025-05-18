"""
Run the Flask application.
"""

import os
from dotenv import load_dotenv
from app import create_app
from config import config

# Load environment variables from .env file
load_dotenv()

# Get environment configuration from environment variable or default to development
env = os.environ.get('FLASK_ENV', 'default')
app = create_app(config[env])

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port) 