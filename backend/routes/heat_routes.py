from flask import Blueprint

from models.heat import HeatZone
from utils.response import ok

heat_bp = Blueprint("heat", __name__, url_prefix="/api")


@heat_bp.route("/heat-zones", methods=["GET"])
def list_heat_zones():
    """Backs useHeatZones()."""
    zones = HeatZone.query.order_by(HeatZone.id).all()
    return ok("Heat zones fetched.", [z.to_dict() for z in zones])
