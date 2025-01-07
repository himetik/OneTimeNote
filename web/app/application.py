import os
import sys
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from loguru import logger
from web.app.routes import note_bp
from web.app.error_handlers import ErrorHandler


def create_app() -> Flask:
    try:
        app = Flask(
            __name__,
            static_folder='../static',
            template_folder="../templates"
        )
        app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
        configure_limiter(app)
        configure_error_handlers(app)
        register_routes(app)
        return app
    except Exception as error:
        logger.critical(f"Error while creating app: {error}")
        raise


def configure_limiter(app: Flask) -> None:
    redis_url = os.getenv("REDIS_URL", "memory://")
    Limiter(
        get_remote_address,
        app=app,
        default_limits=["3 per second"],
        storage_uri=redis_url,
        headers_enabled=True
    )


def configure_error_handlers(app: Flask) -> None:
    ErrorHandler(app)


def register_routes(app: Flask) -> None:
    app.register_blueprint(note_bp)


if __name__ == "__main__":
    try:
        app = create_app()
        app.run(host="127.0.0.1", port=8000)
    except Exception as error:
        logger.critical(f"Critical error while starting application: {error}")
        sys.exit(1)
