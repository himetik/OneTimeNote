from web.app.models import Note
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from loguru import logger


def create_note_in_db(db: Session, note_content: str, temporary_key: str) -> Note:
    try:
        new_note = Note(note=note_content, temporary_key=temporary_key)
        db.add(new_note)
        db.commit()
        return new_note
    except SQLAlchemyError as e:
        logger.error(f"Database error during note creation: {e}")
        db.rollback()
        raise


def get_note_by_temporary_key(db: Session, temporary_key: str) -> Note:
    try:
        return db.query(Note).filter(Note.temporary_key == temporary_key).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error during fetching note: {e}")
        raise


def delete_note_from_db(db: Session, note: Note) -> None:
    try:
        db.delete(note)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error during note deletion: {e}")
        db.rollback()
        raise
