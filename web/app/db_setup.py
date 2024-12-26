import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models import Base


load_dotenv()


DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST', 'database')}:{os.getenv('POSTGRES_PORT', 5432)}/{os.getenv('POSTGRES_DB')}"


engine = create_engine(DATABASE_URL)


def db_setup():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    db_setup()
