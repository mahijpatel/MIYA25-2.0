from flask import Blueprint, current_app, g, request

from models import db
from models.complaint import Complaint
from utils.decorators import optional_auth
from utils.file_upload import save_upload
from utils.response import fail, ok

complaint_bp = Blueprint("complaints", __name__, url_prefix="/api/complaint")


@complaint_bp.route("", methods=["POST"])
@optional_auth
def submit_complaint():
    """POST /complaint - supports JSON or multipart with an optional attachment."""
    try:
        if request.content_type and "multipart/form-data" in request.content_type:
            body = request.form
            attachment = request.files.get("attachment")
        else:
            body = request.get_json(silent=True) or {}
            attachment = None

        title = (body.get("title") or "").strip()
        if not title:
            return fail("A complaint title is required.", 422)

        attachment_filename = ""
        if attachment:
            saved, name_or_error = save_upload(attachment, current_app.config["COMPLAINT_ATTACHMENT_FOLDER"])
            if saved:
                attachment_filename = name_or_error

        user = g.get("current_user")
        complaint = Complaint(
            user_id=user["user_id"] if user else None,
            category=body.get("category", "tree-damage"),
            title=title,
            description=body.get("description", ""),
            location_name=body.get("location_name", "Bhavnagar"),
            latitude=float(body.get("latitude", 21.7645) or 21.7645),
            longitude=float(body.get("longitude", 72.1519) or 72.1519),
            attachment_filename=attachment_filename,
        )
        db.session.add(complaint)
        db.session.commit()
        return ok("Complaint submitted successfully.", complaint.to_dict(), 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not submit complaint: {exc}", 500)


@complaint_bp.route("/status/<int:complaint_id>", methods=["GET"])
@optional_auth
def get_complaint_status(complaint_id):
    """GET /complaint/status/<id>"""
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return fail("Complaint not found.", 404)
    return ok("Complaint status fetched.", complaint.to_dict())


@complaint_bp.route("/mine", methods=["GET"])
@optional_auth
def my_complaints():
    query = Complaint.query
    user = g.get("current_user")
    if user:
        query = query.filter_by(user_id=user["user_id"])
    complaints = query.order_by(Complaint.created_at.desc()).all()
    return ok("Your complaints fetched.", [c.to_dict() for c in complaints])


@complaint_bp.route("/all", methods=["GET"])
@optional_auth
def all_complaints():
    """For gov citizen-complaints dashboard."""
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return ok("All complaints fetched.", [c.to_dict() for c in complaints])
