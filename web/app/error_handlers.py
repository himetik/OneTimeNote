from flask import render_template, jsonify
from werkzeug.exceptions import HTTPException, TooManyRequests


class ErrorHandler:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.register_error_handler(404, self.handle_404)
        app.register_error_handler(500, self.handle_500)
        app.register_error_handler(TooManyRequests, self.handle_429)
        app.register_error_handler(Exception, self.handle_exception)

    def handle_404(self, error):
        return render_template("404.html"), 404

    def handle_500(self, error):
        return render_template("500.html"), 500

    def handle_429(self, error):
        return jsonify({
            "success": False,
            "error": "Too many requests.",
            "retry_after": error.description if hasattr(error, "description") else None
        }), 429

    def handle_exception(self, error):
        if isinstance(error, HTTPException):
            return jsonify({
                "success": False,
                "error": error.description
            }), error.code
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500
