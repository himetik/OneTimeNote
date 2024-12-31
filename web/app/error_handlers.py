from flask import render_template, jsonify


class ErrorHandler:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.register_error_handler(404, self.handle_404)
        app.register_error_handler(500, self.handle_500)
        app.register_error_handler(Exception, self.handle_exception)

    def handle_404(self, error):
        return render_template("404.html"), 404

    def handle_500(self, error):
        return render_template("500.html"), 500

    def handle_exception(self, error):
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500
