from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URL = (f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
MAX_NOTE_LENGTH = os.getenv("MAX_NOTE_LENGTH")
RATE_LIMIT = os.getenv("RATE_LIMIT")
