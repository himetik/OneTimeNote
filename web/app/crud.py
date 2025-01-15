from sqlalchemy.orm import Session
from web.app.models import Note
from sqlalchemy.sql import text


def create_note_in_db(db: Session, note_content: str, temporary_key: str) -> Note:
    new_note = Note(note=note_content, temporary_key=temporary_key)
    db.add(new_note)
    db.commit()
    return new_note


def get_note_by_temporary_key(db: Session, temporary_key: str) -> Note:
    return db.query(Note).filter(Note.temporary_key == temporary_key).first()


def delete_note_from_db(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()


def update_note_confirmation(db, temporary_key):
    query = text("UPDATE notes SET is_confirmed = TRUE WHERE temporary_key = :temporary_key")
    db.execute(query, {"temporary_key": temporary_key})
    db.commit()
