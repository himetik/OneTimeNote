from typing import Optional
from web.app.models import Note


class NoteService:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_note(self, note_content: str, temporary_key: str) -> Note:
        with self.db_session() as db:
            new_note = Note(note=note_content, temporary_key=temporary_key)
            db.add(new_note)
            db.commit()
            return new_note

    def get_note(self, temporary_key: str) -> Optional[Note]:
        with self.db_session() as db:
            return db.query(Note).filter(Note.temporary_key == temporary_key).first()

    def delete_note(self, note: Note) -> None:
        with self.db_session() as db:
            db.delete(note)
            db.commit()
