from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from web.app.init_database import Base


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    note = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    temporary_key = Column(String, unique=True, nullable=False)
