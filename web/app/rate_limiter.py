import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from web.app.config import RATE_LIMIT


def configure_limiter(app):
    redis_url = os.getenv("REDIS_URL")
    Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits = [RATE_LIMIT],
        storage_uri=redis_url,
        headers_enabled=True
    )
