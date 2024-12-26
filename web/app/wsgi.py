from web.app.application import app
from loguru import logger


if __name__ == "__main__":
    try:
        app.run()
    except Exception as error:
        logger.critical(f"Critical error while running the application: {error}")
        raise
