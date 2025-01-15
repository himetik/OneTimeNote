from flask import Blueprint, abort, render_template, request, jsonify, g, redirect, url_for
from web.app.crud import NoteService
from web.app.database import get_db
from sqlalchemy.sql import text


note_bp = Blueprint('notes', __name__)


@note_bp.before_request
def set_db_session():
    g.db = next(get_db())
    g.note_service = NoteService(g.db)


@note_bp.teardown_request
def close_db_session(exception=None):
    db = g.pop('db', None)
    if db:
        db.close()


def get_valid_note(temporary_key):
    note = g.note_service.get_note_by_temporary_key(temporary_key)
    if not note:
        abort(404)
    return note


@note_bp.route("/", methods=["GET"])
def get_creation_page():
    return render_template("create-note.html")


@note_bp.route("/creation", methods=["POST"])
def post_note():
    json_data = request.get_json()
    g.note_service.create_note(json_data.get("note"), json_data.get("temporary_key"))
    return jsonify({"success": True}), 201


@note_bp.route("/confirm/<temporary_key>/<secret_part>", methods=["GET"])
def get_confirmation(temporary_key, secret_part):
    note = get_valid_note(temporary_key)
    if note.is_confirmed:
        return redirect(url_for('notes.get_note_by_key', temporary_key=temporary_key, secret_part=secret_part))
    return render_template("confirm-view-note.html", temporary_key=temporary_key, secret_part=secret_part)


@note_bp.route("/confirm/<temporary_key>/<secret_part>", methods=["POST"])
def post_confirmation(temporary_key, secret_part):
    note = get_valid_note(temporary_key)
    if not note.is_confirmed:
        g.note_service.update_note_confirmation(temporary_key)
    return redirect(url_for('notes.get_note_by_key', temporary_key=temporary_key, secret_part=secret_part))


@note_bp.route("/view/<temporary_key>/<secret_part>", methods=["GET"])
def get_note_by_key(temporary_key, secret_part):
    note = get_valid_note(temporary_key)
    if not note.is_confirmed:
        return redirect(url_for('notes.get_confirmation', temporary_key=temporary_key, secret_part=secret_part))
    encrypted_note = note.note
    g.note_service.delete_note(note)
    return render_template("view-note.html", encrypted_note=encrypted_note)


@note_bp.route("/health", methods=["GET"])
def health_check():
    g.db.execute(text('SELECT 1'))
    return jsonify({"status": "healthy"}), 200
