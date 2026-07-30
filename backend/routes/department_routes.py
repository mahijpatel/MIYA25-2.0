from flask import Blueprint

from models.department import Department
from utils.response import ok

department_bp = Blueprint("departments", __name__, url_prefix="/api")


@department_bp.route("/departments", methods=["GET"])
def list_departments():
    """Backs useDepartments()."""
    departments = Department.query.order_by(Department.id).all()
    return ok("Departments fetched.", [d.to_dict() for d in departments])
