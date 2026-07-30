from flask import Blueprint, current_app, g, request

from models import db
from models.emergency import EmergencyReport
from utils.decorators import optional_auth
from utils.file_upload import save_upload
from utils.response import fail, ok

emergency_bp = Blueprint("emergency", __name__, url_prefix="/api")


@emergency_bp.route("/emergency-reports", methods=["GET"])
@optional_auth
def list_emergency_reports():
    """Backs useEmergencyReports()."""
    query = EmergencyReport.query
    status = request.args.get("status")
    category = request.args.get("category")
    if status:
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
    reports = query.order_by(EmergencyReport.created_at.desc()).all()
    return ok("Emergency reports fetched.", [r.to_dict() for r in reports])


@emergency_bp.route("/emergency-reports", methods=["POST"])
@optional_auth
def create_emergency_report():
    """Backs useCreateEmergencyReport(). Accepts JSON or multipart with an optional attachment."""
    try:
        if request.content_type and "multipart/form-data" in request.content_type:
            body = request.form
            attachment = request.files.get("attachment")
        else:
            body = request.get_json(silent=True) or {}
            attachment = None

        title = (body.get("title") or "").strip()
        if not title:
            return fail("A title/summary is required to submit an emergency report.", 422)

        attachment_filename = ""
        if attachment:
            saved, name_or_error = save_upload(attachment, current_app.config["UPLOAD_FOLDER"])
            if saved:
                attachment_filename = name_or_error

        user = g.get("current_user")
        report = EmergencyReport(
            user_id=user["user_id"] if user else None,
            category=body.get("category", "fire"),
            title=title,
            description=body.get("description", ""),
            latitude=float(body.get("latitude", 21.7645) or 21.7645),
            longitude=float(body.get("longitude", 72.1519) or 72.1519),
            location_name=body.get("location_name", "Bhavnagar"),
            severity=body.get("severity", "medium"),
            attachment_filename=attachment_filename,
        )
        db.session.add(report)
        db.session.commit()
        return ok("Emergency report submitted. Help is on the way.", report.to_dict(), 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not submit emergency report: {exc}", 500)
