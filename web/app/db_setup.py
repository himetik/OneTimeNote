import os
from dotenv import load_dotenv
from loguru import logger
from web.app.logging import setup_logging

setup_logging()

def get_database_url():
    try:
        load_dotenv()

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST", "database")
        port = os.getenv("POSTGRES_PORT", 5432)
        db_name = os.getenv("POSTGRES_DB")

        if not all([user, password, db_name]):
            raise ValueError("Missing required environment variables: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.")

        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    except Exception as error:
        logger.error(f"Error while getting the database URL: {error}")
        return None


DATABASE_URL = get_database_url()
