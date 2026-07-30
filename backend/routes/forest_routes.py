from flask import Blueprint, request

from models.forest import ForestSite
from utils.response import fail, ok

forest_bp = Blueprint("forests", __name__, url_prefix="/api")


@forest_bp.route("/forests", methods=["GET"])
def list_forests():
    """Backs useForestSites()."""
    sites = ForestSite.query.order_by(ForestSite.id).all()
    return ok("Forest sites fetched.", [s.to_dict() for s in sites])


@forest_bp.route("/forests/<int:site_id>", methods=["GET"])
def get_forest(site_id):
    """Backs useForestSite(id) used on /citizen/forest/[id]."""
    site = ForestSite.query.get(site_id)
    if not site:
        return fail("Forest site not found.", 404)
    return ok("Forest site fetched.", site.to_dict())
