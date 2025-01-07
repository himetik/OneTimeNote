from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from loguru import logger
import os
from dotenv import load_dotenv


def get_database_url():
    try:
        load_dotenv()

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST", "database")
        port = os.getenv("POSTGRES_PORT", 5432)
        db_name = os.getenv("POSTGRES_DB", "OTNWSDB")

        if not user or not password or not db_name:
            missing_vars = [
                var for var, value in {
                    "POSTGRES_USER": user,
                    "POSTGRES_PASSWORD": password,
                    "POSTGRES_DB": db_name,
                }.items() if not value
            ]
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}.")

        database_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        logger.info("DATABASE_URL successfully constructed.")
        return database_url

    except Exception as error:
        logger.error(f"Error constructing DATABASE_URL: {error}")
        raise


def create_engine_and_session(database_url):
    try:
        if not database_url:
            raise ValueError("DATABASE_URL is missing or empty.")

        engine = create_engine(database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        logger.info("SQLAlchemy engine and sessionmaker successfully configured.")
        return engine, SessionLocal, Base

    except Exception as error:
        logger.error(f"Error configuring SQLAlchemy engine: {error}")
        raise


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as error:
        logger.error(f"Error during database session: {error}")
        raise
    finally:
        try:
            db.close()
        except Exception as error:
            logger.error(f"Error closing database session: {error}")


try:
    DATABASE_URL = get_database_url()
    engine, SessionLocal, Base = create_engine_and_session(DATABASE_URL)
except Exception as error:
    logger.critical(f"Failed to configure the database: {error}")
    raise
