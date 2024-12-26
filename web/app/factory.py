import os
import sys
from flask import Flask
from web.app.routes import configure_routes


def make_app():
    try:
        app = Flask(__name__, static_folder='../static', template_folder="../templates")
        app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
        configure_routes(app)
        return app
    except Exception as error:
        print(f"Error during app creation: {error}", file=sys.stderr)
        sys.exit(1)
