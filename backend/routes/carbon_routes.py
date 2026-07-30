from flask import Blueprint, g, request

from models import db
from models.carbon import CarbonLog
from utils.decorators import optional_auth
from utils.response import fail, ok

carbon_bp = Blueprint("carbon", __name__, url_prefix="/api")


@carbon_bp.route("/carbon-logs", methods=["GET"])
@optional_auth
def list_carbon_logs():
    """Backs useCarbonLogs()."""
    query = CarbonLog.query
    user = g.get("current_user")
    if user:
        query = query.filter_by(user_id=user["user_id"])
    logs = query.order_by(CarbonLog.created_at.desc()).limit(50).all()
    return ok("Carbon logs fetched.", [log.to_dict() for log in logs])


@carbon_bp.route("/carbon-logs", methods=["POST"])
@optional_auth
def save_carbon_log():
    """Backs useSaveCarbonLog()."""
    try:
        body = request.get_json(silent=True) or {}
        transport_kg = float(body.get("transport_kg", 0) or 0)
        electricity_kg = float(body.get("electricity_kg", 0) or 0)
        diet_kg = float(body.get("diet_kg", 0) or 0)
        waste_kg = float(body.get("waste_kg", 0) or 0)
        total_kg = transport_kg + electricity_kg + diet_kg + waste_kg

        user = g.get("current_user")
        log = CarbonLog(
            user_id=user["user_id"] if user else None,
            transport_kg=transport_kg,
            electricity_kg=electricity_kg,
            diet_kg=diet_kg,
            waste_kg=waste_kg,
            total_kg=total_kg,
            diet_type=body.get("diet_type", "mixed"),
        )
        db.session.add(log)
        db.session.commit()
        return ok("Carbon log saved.", log.to_dict(), 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not save carbon log: {exc}", 500)
