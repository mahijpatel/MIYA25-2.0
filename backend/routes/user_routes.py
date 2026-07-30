from flask import Blueprint, request

from models import db
from models.user import User
from utils.decorators import role_required
from utils.response import fail, ok

user_bp = Blueprint("users", __name__, url_prefix="/api")


@user_bp.route("/users", methods=["GET"])
@role_required("admin", "gov")
def list_users():
    """Backs useUsers()."""
    query = User.query
    role = request.args.get("role")
    if role:
        query = query.filter_by(role=role)
    users = query.order_by(User.created_at.desc()).all()
    return ok("Users fetched.", [u.to_public_dict() for u in users])


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@role_required("admin", "gov")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return fail("User not found.", 404)
    return ok("User fetched.", user.to_public_dict())


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@role_required("admin")
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return fail("User not found.", 404)

        body = request.get_json(silent=True) or {}
        for field in ("name", "phone", "city", "role", "is_active"):
            if field in body:
                setattr(user, field, body[field])

        db.session.commit()
        return ok("User updated.", user.to_public_dict())
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not update user: {exc}", 500)
