from flask import Blueprint, g, request

from models import db
from models.volunteer import Volunteer, VolunteerSignup
from utils.decorators import optional_auth
from utils.response import fail, ok

volunteer_bp = Blueprint("volunteers", __name__, url_prefix="/api")


@volunteer_bp.route("/volunteers", methods=["GET"])
def list_volunteer_opportunities():
    """Backs useVolunteers()."""
    opportunities = Volunteer.query.order_by(Volunteer.date.asc()).all()
    result = []
    for v in opportunities:
        data = v.to_dict()
        data["slots_available"] = max(v.slots_total - v.slots_filled, 0)
        result.append(data)
    return ok("Volunteer opportunities fetched.", result)


@volunteer_bp.route("/volunteer-signups", methods=["POST"])
@optional_auth
def signup_for_volunteer():
    """Backs useVolunteerSignup()."""
    try:
        body = request.get_json(silent=True) or {}
        volunteer_id = body.get("volunteer_id")
        opportunity = Volunteer.query.get(volunteer_id) if volunteer_id else None
        if not opportunity:
            return fail("Volunteer opportunity not found.", 404)

        if opportunity.slots_filled >= opportunity.slots_total:
            status = "waitlisted"
        else:
            status = "confirmed"
            opportunity.slots_filled += 1

        user = g.get("current_user")
        signup = VolunteerSignup(
            volunteer_id=opportunity.id,
            user_id=user["user_id"] if user else None,
            full_name=body.get("full_name", user["name"] if user else "Guest Volunteer"),
            phone=body.get("phone", ""),
            status=status,
        )
        db.session.add(signup)
        db.session.commit()
        message = "You're signed up!" if status == "confirmed" else "Opportunity full - you've been waitlisted."
        return ok(message, signup.to_dict(), 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not complete signup: {exc}", 500)


@volunteer_bp.route("/volunteer-signups/mine", methods=["GET"])
@optional_auth
def my_volunteer_signups():
    """Backs useMyVolunteerSignups()."""
    query = VolunteerSignup.query
    user = g.get("current_user")
    if user:
        query = query.filter_by(user_id=user["user_id"])
    signups = query.order_by(VolunteerSignup.created_at.desc()).all()
    return ok("Your volunteer signups fetched.", [s.to_dict() for s in signups])
