from flask import Blueprint, request

from models.audit import AuditLog
from utils.decorators import role_required
from utils.response import ok

audit_bp = Blueprint("audit", __name__, url_prefix="/api")


@audit_bp.route("/audit-logs", methods=["GET"])
@role_required("admin", "gov")
def list_audit_logs():
    """Backs useAuditLogs()."""
    limit = request.args.get("limit", default=100, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    return ok("Audit logs fetched.", [log.to_dict() for log in logs])
