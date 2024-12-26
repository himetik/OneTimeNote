from loguru import logger
import os


def setup_logging():
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)

    logger.add(
        os.path.join(LOG_DIR, "errors.log"),
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        retention="1 days",
        compression="zip"
    )
