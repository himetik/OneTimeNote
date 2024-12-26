from flask import render_template, request, jsonify, make_response, redirect, url_for
from sqlalchemy.orm import Session
from web.app.models import Note
from web.app.database import get_db


def configure_routes(app):
    @app.errorhandler(404)
    def handle_404(error):
        return render_template("404.html"), 404

    @app.route("/create_note", methods=["GET", "POST"])
    @app.route("/", methods=["GET", "POST"])
    def create_note():
        db: Session = next(get_db())
        try:
            if request.method == "GET":
                return render_template("create-note.html")

            if request.method == "POST":
                data = request.get_json()
                note_content = data.get("note")
                secret_part = data.get("secret_part")
                temporary_key = data.get("temporary_key")

                if not note_content or not secret_part or not temporary_key:
                    return jsonify({"success": False, "error": "Note, secret part, and temporary key are required"}), 400

                new_note = Note(note=note_content, temporary_key=temporary_key)
                db.add(new_note)
                db.commit()

                return jsonify({"success": True}), 201

        except Exception as e:
            print(f"Error saving note: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

        finally:
            db.close()

    @app.route("/notes/<temporary_key>/<secret_part>", methods=["GET"])
    def redirect_to_confirm(temporary_key, secret_part):
        return redirect(url_for('confirm_view', temporary_key=temporary_key, secret_part=secret_part))

    @app.route("/confirm/<temporary_key>/<secret_part>", methods=["GET"])
    def confirm_view(temporary_key, secret_part):
        db: Session = next(get_db())
        try:
            note = db.query(Note).filter(Note.temporary_key == temporary_key).first()

            if not note:
                return render_template("404.html"), 404

            return render_template("confirm-view-note.html", temporary_key=temporary_key, secret_part=secret_part)

        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({"success": False, "error": f"Error fetching note: {str(e)}"}), 500

        finally:
            db.close()

    @app.route("/view/<temporary_key>/<secret_part>", methods=["GET"])
    def get_note_by_key(temporary_key, secret_part):
        db: Session = next(get_db())
        try:
            note = db.query(Note).filter(Note.temporary_key == temporary_key).first()

            if not note:
                return render_template("404.html"), 404

            encrypted_note = note.note
            db.delete(note)
            db.commit()

            response = make_response(render_template("view-note.html", encrypted_note=encrypted_note))
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({"success": False, "error": f"Error fetching note: {str(e)}"}), 500

        finally:
            db.close()
