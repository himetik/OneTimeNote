import os
import sys
from loguru import logger
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from web.app.routes import note_bp
from web.app.error_handlers import ErrorHandler


def make_app():
    try:
        app = Flask(__name__, 
                   static_folder='../static', 
                   template_folder="../templates")
        app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
        redis_url = os.getenv("REDIS_URL")
        Limiter(
            get_remote_address,
            app=app,
            default_limits=["3 per second"],
            storage_uri=redis_url,
            headers_enabled=True
        )
        ErrorHandler(app)
        app.register_blueprint(note_bp)
        return app
    except Exception as error:
        logger.critical(f"Error during app creation: {error}")
        sys.exit(1)


try:
    app = make_app()
except Exception as error:
    logger.critical(f"Critical error during application initialization: {error}")
    sys.exit(1)


if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=8000)
    except Exception as error:
        logger.critical(f"Critical error while running the application: {error}")
        sys.exit(1)
