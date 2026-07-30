from flask import Blueprint

from models.drone import DroneMission
from utils.response import ok

drone_bp = Blueprint("drones", __name__, url_prefix="/api")


@drone_bp.route("/drone-missions", methods=["GET"])
def list_drone_missions():
    """Backs useDroneMissions()."""
    missions = DroneMission.query.order_by(DroneMission.scheduled_at.desc()).all()
    return ok("Drone missions fetched.", [m.to_dict() for m in missions])
