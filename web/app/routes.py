from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for, g
from loguru import logger
from web.app.database import get_db
from web.app.config import MAX_NOTE_LENGTH
from web.app.note_service import create_note_in_db, get_note_by_temporary_key, delete_note_from_db
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError


note_bp = Blueprint('notes', __name__)


@note_bp.before_request
def set_db_session():
    try:
        g.db = next(get_db())
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при создании сессии базы данных: {e}")
        return jsonify({"success": False, "error": "Ошибка подключения к базе данных"}), 500


@note_bp.teardown_request
def close_db_session(exception=None):
    db = g.get('db', None)
    if db:
        try:
            db.close()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при закрытии сессии базы данных: {e}")


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

        create_note_in_db(g.db, note_content, temporary_key)
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
        note = get_note_by_temporary_key(g.db, temporary_key)
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
        note = get_note_by_temporary_key(g.db, temporary_key)
        if not note:
            return render_template("404.html"), 404
        encrypted_note = note.note
        response = make_response(
            render_template("view-note.html", encrypted_note=encrypted_note)
        )
        delete_note_from_db(g.db, note)
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
        g.db.execute(text('SELECT 1'))
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
