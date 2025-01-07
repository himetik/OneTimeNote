from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from web.app.db_setup import DATABASE_URL
from loguru import logger


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
