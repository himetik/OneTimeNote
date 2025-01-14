from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
MAX_NOTE_LENGTH = os.getenv("MAX_NOTE_LENGTH")
RATE_LIMIT = os.getenv("RATE_LIMIT")
