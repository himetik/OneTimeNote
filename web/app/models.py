from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    note = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime)
    temporary_key = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Note(id={self.id}, created_at={self.created_at})>"
