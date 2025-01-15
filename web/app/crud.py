from sqlalchemy.orm import Session
from web.app.models import Note


class NoteService:
    def __init__(self, db: Session):
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
