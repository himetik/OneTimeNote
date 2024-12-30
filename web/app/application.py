import sys
from web.app.factory import make_app
from loguru import logger


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
