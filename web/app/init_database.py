from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from web.app.config import DATABASE_URL


Base = declarative_base()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
