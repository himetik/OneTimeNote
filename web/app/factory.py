import os
import sys
from flask import Flask
from loguru import logger
from web.app.routes import note_bp
from web.app.error_handlers import ErrorHandler


def make_app():
    try:
        app = Flask(__name__, 
                   static_folder='../static', 
                   template_folder="../templates")
        app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
        ErrorHandler(app)
        app.register_blueprint(note_bp)
        return app
    except Exception as error:
        logger.critical(f"Error during app creation: {error}")
        sys.exit(1)
