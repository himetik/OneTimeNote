from flask import render_template, request, jsonify, make_response, redirect, url_for
from loguru import logger
from web.app.models import Note
from web.app.database import get_db
from contextlib import contextmanager


def configure_routes(app):

    @contextmanager
    def get_db_session():
        db = next(get_db())
        try:
            yield db
        finally:
            db.close()

    @app.errorhandler(404)
    def handle_404(error):
        logger.error(f"404 Error: {error}")
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def handle_500(error):
        logger.error(f"500 Error: {error}")
        return render_template("500.html"), 500

    @app.after_request
    def set_no_cache_headers(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route("/", methods=["GET"])
    def show_create_note_page():
        return render_template("create-note.html")

    @app.route("/creation", methods=["POST"])
    def create_note():
        try:
            data = request.get_json()
            note_content = data.get("note")
            secret_part = data.get("secret_part")
            temporary_key = data.get("temporary_key")

            if not note_content or not secret_part or not temporary_key:
                return jsonify({"success": False, "error": "Note, secret part, and temporary key are required"}), 400

            with get_db_session() as db:
                new_note = Note(note=note_content, temporary_key=temporary_key)
                db.add(new_note)
                db.commit()

            return jsonify({"success": True}), 201

        except Exception as e:
            logger.error(f"Error saving note: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/notes/<temporary_key>/<secret_part>", methods=["GET"])
    def redirect_to_confirm(temporary_key, secret_part):
        if len(temporary_key) != 16 or len(secret_part) != 64:
            logger.warning("Invalid key length")
            return render_template("404.html"), 404
        return redirect(url_for('confirm_view', temporary_key=temporary_key, secret_part=secret_part))

    @app.route("/confirm/<temporary_key>/<secret_part>", methods=["GET"])
    def confirm_view(temporary_key, secret_part):
        try:
            with get_db_session() as db:
                note = db.query(Note).filter(Note.temporary_key == temporary_key).first()

                if not note:
                    return render_template("404.html"), 404

            return render_template("confirm-view-note.html", temporary_key=temporary_key, secret_part=secret_part)

        except Exception as e:
            logger.error(f"Database error: {e}")
            return jsonify({"success": False, "error": f"Error fetching note: {str(e)}"}), 500

    @app.route("/view/<temporary_key>/<secret_part>", methods=["GET"])
    def get_note_by_key(temporary_key, secret_part):
        try:
            with get_db_session() as db:
                note = db.query(Note).filter(Note.temporary_key == temporary_key).first()

                if not note:
                    return render_template("404.html"), 404

                encrypted_note = note.note
                db.delete(note)
                db.commit()

                response = make_response(render_template("view-note.html", encrypted_note=encrypted_note))
                return response

        except Exception as e:
            logger.error(f"Database error: {e}")
            return jsonify({"success": False, "error": f"Error fetching note: {str(e)}"}), 500
