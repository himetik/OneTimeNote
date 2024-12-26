from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from web.app.db_setup import DATABASE_URL
from loguru import logger
from web.app.logging import setup_logging

setup_logging()

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as error:
    logger.error(f"Failed to configure database engine: {error}")
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
            logger.error(f"Error while closing database session: {error}")


def db_setup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as error:
        logger.error(f"Error during database setup: {error}")
        raise


if __name__ == "__main__":
    try:
        db_setup()
    except Exception as error:
        logger.critical(f"Critical error during database initialization: {error}")
        raise
