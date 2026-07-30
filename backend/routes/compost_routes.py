from flask import Blueprint

from models.compost import CompostUnit
from utils.response import ok

compost_bp = Blueprint("compost", __name__, url_prefix="/api")


@compost_bp.route("/compost-units", methods=["GET"])
def list_compost_units():
    """Backs useCompostUnits()."""
    units = CompostUnit.query.order_by(CompostUnit.id).all()
    return ok("Compost units fetched.", [u.to_dict() for u in units])
