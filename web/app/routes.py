from flask import render_template


def configure_routes(app):
    @app.errorhandler(404)
    def handle_404(error):
        return render_template("404.html"), 404
