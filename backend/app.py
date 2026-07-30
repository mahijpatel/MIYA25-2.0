"""
MIYA25 backend entrypoint.

Run with:
    python app.py

The app will:
  1. Create the SQLite database file and tables if they don't exist.
  2. Seed lightweight demo data (users, trees, forests, rewards, etc.)
     the very first time it runs, so the frontend has something to show
     immediately.
  3. Serve the REST API on http://localhost:5000
"""

import os

from flask import Flask
from flask_cors import CORS

from config import Config
from models import db
from routes import register_routes
from utils.response import fail, ok


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Make sure upload directories exist even on a fresh clone.
    for folder in (
        app.config["UPLOAD_FOLDER"],
        app.config["PROFILE_PHOTO_FOLDER"],
        app.config["PLANT_IMAGE_FOLDER"],
        app.config["COMPLAINT_ATTACHMENT_FOLDER"],
    ):
        os.makedirs(folder, exist_ok=True)

    db.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    register_routes(app)

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return ok("MIYA25 backend is running.", {"status": "healthy"})

    @app.errorhandler(404)
    def not_found(_error):
        return fail("The requested endpoint does not exist.", 404)

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return fail("This HTTP method is not allowed on this endpoint.", 405)

    @app.errorhandler(413)
    def file_too_large(_error):
        return fail("File is too large. Maximum upload size is 10MB.", 413)

    @app.errorhandler(500)
    def internal_error(_error):
        return fail("An unexpected server error occurred.", 500)

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    return app


def _seed_if_empty():
    """Runs the seed script only if the database is empty, so re-running
    `python app.py` never duplicates demo data."""
    from models.user import User

    if User.query.first() is None:
        from seed import run_seed

        run_seed(db)


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
