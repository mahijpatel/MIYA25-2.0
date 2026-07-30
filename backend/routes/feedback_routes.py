from flask import Blueprint, g, request

from models import db
from models.feedback import Feedback
from utils.decorators import optional_auth
from utils.response import fail, ok

feedback_bp = Blueprint("feedback", __name__, url_prefix="/api/feedback")


@feedback_bp.route("", methods=["POST"])
@optional_auth
def submit_feedback():
    try:
        body = request.get_json(silent=True) or {}
        message = (body.get("message") or "").strip()
        if not message:
            return fail("Feedback message is required.", 422)

        user = g.get("current_user")
        feedback = Feedback(
            user_id=user["user_id"] if user else None,
            subject=body.get("subject", "General Feedback"),
            message=message,
            rating=int(body.get("rating", 5) or 5),
        )
        db.session.add(feedback)
        db.session.commit()
        return ok("Thank you for your feedback!", feedback.to_dict(), 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not submit feedback: {exc}", 500)


@feedback_bp.route("", methods=["GET"])
@optional_auth
def list_feedback():
    query = Feedback.query
    user = g.get("current_user")
    if user and user.get("role") not in ("admin", "gov"):
        query = query.filter_by(user_id=user["user_id"])
    records = query.order_by(Feedback.created_at.desc()).all()
    return ok("Feedback fetched.", [f.to_dict() for f in records])
