from flask import Blueprint, g, request

from models import db
from models.notification import Notification
from utils.decorators import optional_auth
from utils.response import fail, ok

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")


@notification_bp.route("", methods=["GET"])
@optional_auth
def list_notifications():
    query = Notification.query
    user = g.get("current_user")
    if user:
        query = query.filter(
            (Notification.user_id == user["user_id"]) | (Notification.user_id.is_(None))
        )
    else:
        query = query.filter(Notification.user_id.is_(None))
    notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
    return ok("Notifications fetched.", [n.to_dict() for n in notifications])


@notification_bp.route("/<int:notification_id>/read", methods=["POST"])
@optional_auth
def mark_as_read(notification_id):
    try:
        notification = Notification.query.get(notification_id)
        if not notification:
            return fail("Notification not found.", 404)
        notification.is_read = True
        db.session.commit()
        return ok("Notification marked as read.", notification.to_dict())
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not update notification: {exc}", 500)


@notification_bp.route("/read-all", methods=["POST"])
@optional_auth
def mark_all_as_read():
    try:
        user = g.get("current_user")
        query = Notification.query
        if user:
            query = query.filter(
                (Notification.user_id == user["user_id"]) | (Notification.user_id.is_(None))
            )
        else:
            query = query.filter(Notification.user_id.is_(None))
        query.update({"is_read": True})
        db.session.commit()
        return ok("All notifications marked as read.")
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not update notifications: {exc}", 500)
