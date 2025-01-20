# Model and service are duplicated to isolate tests
# Update this code when the source models change

import pytest
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone


Base = declarative_base()


# Duplicate the Note model for tests
class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    note = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    temporary_key = Column(String, unique=True, nullable=False)
    is_confirmed = Column(Boolean, nullable=False, default=False)


# Duplicate NoteService for tests
class NoteService:
    def __init__(self, db):
        self.db = db

    def create_note(self, note_content: str, temporary_key: str) -> Note:
        new_note = Note(note=note_content, temporary_key=temporary_key)
        self.db.add(new_note)
        self.db.commit()
        return new_note

    def get_note_by_temporary_key(self, temporary_key: str) -> Note:
        return self.db.query(Note).filter(Note.temporary_key == temporary_key).first()

    def delete_note(self, note: Note) -> None:
        self.db.delete(note)
        self.db.commit()

    def update_note_confirmation(self, temporary_key: str) -> None:
        self.db.query(Note).filter(Note.temporary_key == temporary_key).update({"is_confirmed": True})
        self.db.commit()


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def note_service(test_db):
    return NoteService(db=test_db)


def test_create_note(note_service):
    note_content = "Scientists often derive new theories from experimental data."
    temporary_key = ""

    new_note = note_service.create_note(note_content, temporary_key)

    assert new_note.note == note_content
    assert new_note.temporary_key == temporary_key


def test_get_note_by_temporary_key(note_service):
    note_content = "Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing a business function outside the user's limits."
    temporary_key = "temp123"

    note_service.create_note(note_content, temporary_key)

    fetched_note = note_service.get_note_by_temporary_key(temporary_key)

    assert fetched_note is not None
    assert fetched_note.note == note_content
    assert fetched_note.temporary_key == temporary_key


def test_delete_note(note_service):
    note_content = "The project failed due to a lack of funding, which made it impossible to purchase the necessary materials and hire skilled workers."
    temporary_key = "temp123"

    new_note = note_service.create_note(note_content, temporary_key)

    note_service.delete_note(new_note)

    deleted_note = note_service.get_note_by_temporary_key(temporary_key)
    assert deleted_note is None


def test_update_note_confirmation(note_service):
    note_content = "The committee couldn't agree on the budget allocation, so they fudged a compromise to avoid further delays."
    temporary_key = "temp123"

    note_service.create_note(note_content, temporary_key)

    note_service.update_note_confirmation(temporary_key)

    updated_note = note_service.get_note_by_temporary_key(temporary_key)
    assert updated_note.is_confirmed
