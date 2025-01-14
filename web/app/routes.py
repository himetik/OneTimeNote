from flask import Blueprint, abort, render_template, request, jsonify, make_response, redirect, url_for, g
from functools import wraps
from web.app.database import get_db
from web.app.note_service import create_note_in_db, get_note_by_temporary_key, delete_note_from_db
from sqlalchemy.sql import text


note_bp = Blueprint('notes', __name__)


def validate_note(f):
    @wraps(f)
    def decorated_function(temporary_key, secret_part):
        note = get_note_by_temporary_key(g.db, temporary_key)
        if not note:
            abort(404)
        return f(temporary_key, secret_part, note)
    return decorated_function


@note_bp.before_request
def set_db_session():
    g.db = next(get_db())


@note_bp.teardown_request
def close_db_session(exception=None):
    db = g.get('db', None)
    if db:
        db.close()


@note_bp.route("/", methods=["GET"])
def show_create_note_page():
    return render_template("create-note.html")


@note_bp.route("/creation", methods=["POST"])
def create_note():
    data = request.get_json()
    note_content = data.get("note")
    temporary_key = data.get("temporary_key")
    create_note_in_db(g.db, note_content, temporary_key)
    return jsonify({"success": True}), 201


@note_bp.route("/notes/<temporary_key>/<secret_part>", methods=["GET"])
def redirect_to_confirm(temporary_key, secret_part):
    return redirect(url_for('notes.confirm_view', temporary_key=temporary_key, secret_part=secret_part))


@note_bp.route("/confirm/<temporary_key>/<secret_part>", methods=["GET"])
@validate_note
def confirm_view(temporary_key, secret_part, note):
    return render_template("confirm-view-note.html", temporary_key=temporary_key, secret_part=secret_part)


@note_bp.route("/view/<temporary_key>/<secret_part>", methods=["GET"])
@validate_note
def get_note_by_key(temporary_key, secret_part, note):
    encrypted_note = note.note
    response = make_response(render_template("view-note.html", encrypted_note=encrypted_note))
    delete_note_from_db(g.db, note)
    return response


@note_bp.route("/health", methods=["GET"])
def health_check():
    g.db.execute(text('SELECT 1'))
    return jsonify({"status": "healthy"}), 200
