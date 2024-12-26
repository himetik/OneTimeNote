import os
import sys
from flask import Flask
from web.app.routes import configure_routes
from loguru import logger


def make_app():
    try:
        app = Flask(__name__, static_folder='../static', template_folder="../templates")
        app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
        configure_routes(app)
        return app
    except Exception as error:
        logger.critical(f"Error during app creation: {error}")
        sys.exit(1)
