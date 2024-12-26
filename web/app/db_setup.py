import os
from dotenv import load_dotenv


def get_database_url():
    load_dotenv()

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "database")
    port = os.getenv("POSTGRES_PORT", 5432)
    db_name = os.getenv("POSTGRES_DB")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"


DATABASE_URL = get_database_url()
