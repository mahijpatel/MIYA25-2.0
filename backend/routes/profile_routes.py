from flask import Blueprint, current_app, g, request

from models import db
from models.user import User
from utils.decorators import token_required
from utils.file_upload import save_upload
from utils.response import fail, ok

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("", methods=["GET"])
@token_required
def get_profile():
    user = User.query.get(g.current_user["user_id"])
    if not user:
        return fail("User not found.", 404)
    return ok("Profile fetched.", user.to_public_dict())


@profile_bp.route("", methods=["PUT"])
@token_required
def update_profile():
    try:
        user = User.query.get(g.current_user["user_id"])
        if not user:
            return fail("User not found.", 404)

        body = request.get_json(silent=True) or {}
        for field in ("name", "phone", "city"):
            if field in body and body[field] is not None:
                setattr(user, field, body[field])

        db.session.commit()
        return ok("Profile updated successfully.", user.to_public_dict())
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not update profile: {exc}", 500)


@profile_bp.route("/photo", methods=["POST"])
@token_required
def upload_profile_photo():
    try:
        user = User.query.get(g.current_user["user_id"])
        if not user:
            return fail("User not found.", 404)

        photo = request.files.get("photo") or request.files.get("file")
        saved, name_or_error = save_upload(photo, current_app.config["PROFILE_PHOTO_FOLDER"])
        if not saved:
            return fail(name_or_error, 422)

        user.avatar_url = f"/uploads/profile_photos/{name_or_error}"
        db.session.commit()
        return ok("Profile photo updated.", {"avatar_url": user.avatar_url})
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not upload photo: {exc}", 500)
