import os

from flask import Blueprint, current_app, send_from_directory

from utils.response import fail

# A small blueprint just for serving uploaded files back to the frontend
# (profile photos, plant images, complaint attachments).
uploads_bp = Blueprint("uploads", __name__)


@uploads_bp.route("/uploads/<path:subpath>", methods=["GET"])
def serve_upload(subpath):
    try:
        directory = current_app.config["UPLOAD_FOLDER"]
        full_path = os.path.normpath(os.path.join(directory, subpath))
        if not full_path.startswith(os.path.normpath(directory)):
            return fail("Invalid file path.", 400)
        folder, filename = os.path.split(full_path)
        if not os.path.isfile(full_path):
            return fail("File not found.", 404)
        return send_from_directory(folder, filename)
    except Exception as exc:  # noqa: BLE001
        return fail(f"Could not serve file: {exc}", 500)


def register_routes(app):
    """Registers every blueprint on the Flask app. Called once from app.py."""
    from routes.auth_routes import auth_bp
    from routes.plant_routes import plant_bp
    from routes.tree_routes import tree_bp
    from routes.forest_routes import forest_bp
    from routes.carbon_routes import carbon_bp
    from routes.carbon_credit_routes import carbon_credit_bp
    from routes.emergency_routes import emergency_bp
    from routes.pickup_routes import pickup_bp
    from routes.compost_routes import compost_bp
    from routes.department_routes import department_bp
    from routes.drone_routes import drone_bp
    from routes.flood_routes import flood_bp
    from routes.heat_routes import heat_bp
    from routes.sensor_routes import sensor_bp
    from routes.leaderboard_routes import leaderboard_bp
    from routes.learning_routes import learning_bp
    from routes.volunteer_routes import volunteer_bp
    from routes.hospital_routes import hospital_bp
    from routes.bhavnagar_routes import bhavnagar_bp
    from routes.weather_routes import weather_bp
    from routes.achievement_routes import achievement_bp
    from routes.audit_routes import audit_bp
    from routes.user_routes import user_bp
    from routes.rewards_routes import rewards_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.profile_routes import profile_bp
    from routes.notification_routes import notification_bp
    from routes.feedback_routes import feedback_bp
    from routes.complaint_routes import complaint_bp

    blueprints = [
        auth_bp,
        plant_bp,
        tree_bp,
        forest_bp,
        carbon_bp,
        carbon_credit_bp,
        emergency_bp,
        pickup_bp,
        compost_bp,
        department_bp,
        drone_bp,
        flood_bp,
        heat_bp,
        sensor_bp,
        leaderboard_bp,
        learning_bp,
        volunteer_bp,
        hospital_bp,
        bhavnagar_bp,
        weather_bp,
        achievement_bp,
        audit_bp,
        user_bp,
        rewards_bp,
        dashboard_bp,
        profile_bp,
        notification_bp,
        feedback_bp,
        complaint_bp,
        uploads_bp,
    ]
    for bp in blueprints:
        app.register_blueprint(bp)
