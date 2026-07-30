from datetime import datetime

from flask import Blueprint, g, request

from models import db
from models.pickup import Pickup
from utils.decorators import optional_auth
from utils.response import fail, ok

pickup_bp = Blueprint("pickups", __name__, url_prefix="/api")


@pickup_bp.route("/pickups/mine", methods=["GET"])
@optional_auth
def my_pickups():
    """Backs useMyPickups()."""
    query = Pickup.query
    user = g.get("current_user")
    if user:
        query = query.filter_by(user_id=user["user_id"])
    pickups = query.order_by(Pickup.scheduled_date.desc()).all()
    return ok("Your pickups fetched.", [p.to_dict() for p in pickups])


@pickup_bp.route("/pickups", methods=["POST"])
@optional_auth
def schedule_pickup():
    """Backs useSchedulePickup()."""
    try:
        body = request.get_json(silent=True) or {}
        scheduled_date = body.get("scheduled_date")
        try:
            scheduled_dt = datetime.fromisoformat(scheduled_date) if scheduled_date else datetime.utcnow()
        except ValueError:
            scheduled_dt = datetime.utcnow()

        user = g.get("current_user")
        pickup = Pickup(
            user_id=user["user_id"] if user else None,
            waste_type=body.get("waste_type", "organic"),
            quantity_kg=float(body.get("quantity_kg", 1) or 1),
            address=body.get("address", "Bhavnagar"),
            scheduled_date=scheduled_dt,
        )
        db.session.add(pickup)
        db.session.commit()
        return ok("Pickup scheduled successfully.", pickup.to_dict(), 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not schedule pickup: {exc}", 500)
