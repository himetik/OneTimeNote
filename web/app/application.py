import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from web.app.routes import note_bp
from web.app.error_handlers import ErrorHandler


def configure_limiter(app):
    redis_url = os.getenv("REDIS_URL")
    Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["3 per second"],
        storage_uri=redis_url,
        headers_enabled=True
    )


def create_app():
    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates"
    )
    app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
    configure_limiter(app)
    ErrorHandler(app)
    app.register_blueprint(note_bp)
    return app


app = create_app()
