from web.app.application import app
from loguru import logger


def run_app():
    app.run()


def main():
    try:
        run_app()
    except Exception as error:
        logger.critical(f"Critical error while running the application: {error}")
        raise


if __name__ == "__main__":
    main()
