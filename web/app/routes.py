from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for
from loguru import logger
from contextlib import contextmanager
from web.app.database import get_db
from web.app.models import Note
from web.app.services import NoteService
from web.app.decorators import no_cache
from web.app.config import MAX_NOTE_LENGTH
from sqlalchemy.sql import text


note_bp = Blueprint('notes', __name__)


class NoteController:
    def __init__(self, note_service: NoteService):
        self.note_service = note_service

    def create_note(self, note_content: str, secret_part: str, temporary_key: str) -> tuple:
        if not all([note_content, secret_part, temporary_key]):
            return jsonify({
                "success": False,
                "error": "Note, secret part, and temporary key are required"
            }), 400

        try:
            self.note_service.create_note(note_content, temporary_key)
            return jsonify({"success": True}), 201
        except Exception as e:
            logger.error(f"Error saving note: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    def get_note(self, temporary_key: str, secret_part: str) -> tuple:
        try:
            note = self.note_service.get_note(temporary_key)
            if not note:
                return render_template("404.html"), 404

            response = make_response(
                render_template("view-note.html", encrypted_note=note.note)
            )
            self.note_service.delete_note(note)
            return response
        except Exception as e:
            logger.error(f"Database error: {e}")
            return jsonify({
                "success": False,
                "error": f"Error fetching note: {str(e)}"
            }), 500


@contextmanager
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@note_bp.errorhandler(404)
def handle_404(error):
    logger.error(f"404 Error: {error}")
    return render_template("404.html"), 404


@note_bp.errorhandler(500)
def handle_500(error):
    logger.error(f"500 Error: {error}")
    return render_template("500.html"), 500


@note_bp.after_request
@no_cache
def after_request(response):
    return response


@note_bp.route("/", methods=["GET"])
def show_create_note_page():
    return render_template("create-note.html")


@note_bp.route("/creation", methods=["POST"])
def create_note():
    try:
        data = request.get_json()
        note_content = data.get("note")
        secret_part = data.get("secret_part")
        temporary_key = data.get("temporary_key")
        if note_content and len(note_content) > MAX_NOTE_LENGTH:
            return jsonify({
                "success": False,
                "error": f"The record length exceeds {MAX_NOTE_LENGTH} characters."
            }), 400
        if not all([note_content, secret_part, temporary_key]):
            return jsonify({
                "success": False,
                "error": "Note, secret part, and temporary key are required"
            }), 400
        with get_db_session() as db:
            new_note = Note(note=note_content, temporary_key=temporary_key)
            db.add(new_note)
            db.commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        logger.error(f"Error saving note: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@note_bp.route("/notes/<temporary_key>/<secret_part>", methods=["GET"])
def redirect_to_confirm(temporary_key, secret_part):
    return redirect(url_for('notes.confirm_view',
                          temporary_key=temporary_key,
                          secret_part=secret_part))


@note_bp.route("/confirm/<temporary_key>/<secret_part>", methods=["GET"])
def confirm_view(temporary_key, secret_part):
    try:
        with get_db_session() as db:
            note = db.query(Note).filter(Note.temporary_key == temporary_key).first()
            if not note:
                return render_template("404.html"), 404
        return render_template("confirm-view-note.html",
                             temporary_key=temporary_key,
                             secret_part=secret_part)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            "success": False,
            "error": f"Error fetching note: {str(e)}"
        }), 500


@note_bp.route("/view/<temporary_key>/<secret_part>", methods=["GET"])
def get_note_by_key(temporary_key, secret_part):
    try:
        with get_db_session() as db:
            note = db.query(Note).filter(Note.temporary_key == temporary_key).first()
            if not note:
                return render_template("404.html"), 404
            encrypted_note = note.note
            response = make_response(
                render_template("view-note.html", encrypted_note=encrypted_note)
            )
            db.delete(note)
            db.commit()
            return response
    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            "success": False,
            "error": f"Error fetching note: {str(e)}"
        }), 500

@note_bp.route("/health", methods=["GET"])
def health_check():
    try:
        with get_db_session() as db:
            db.execute(text('SELECT 1'))
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
