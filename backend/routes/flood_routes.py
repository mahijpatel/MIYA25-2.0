from flask import Blueprint

from models.flood import FloodZone
from utils.response import ok

flood_bp = Blueprint("flood", __name__, url_prefix="/api")


@flood_bp.route("/flood-zones", methods=["GET"])
def list_flood_zones():
    """Backs useFloodZones()."""
    zones = FloodZone.query.order_by(FloodZone.id).all()
    return ok("Flood zones fetched.", [z.to_dict() for z in zones])
