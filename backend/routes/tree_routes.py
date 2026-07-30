from datetime import datetime

from flask import Blueprint, g, request

from models import db
from models.tree import Tree
from utils.decorators import optional_auth, token_required
from utils.response import fail, ok

tree_bp = Blueprint("trees", __name__, url_prefix="/api")


@tree_bp.route("/trees", methods=["GET"])
def list_trees():
    """Backs useTrees()."""
    query = Tree.query
    forest_site_id = request.args.get("forest_site_id")
    health_status = request.args.get("health_status")
    if forest_site_id:
        query = query.filter_by(forest_site_id=forest_site_id)
    if health_status:
        query = query.filter_by(health_status=health_status)
    trees = query.order_by(Tree.id.desc()).all()
    return ok("Trees fetched.", [t.to_dict() for t in trees])


@tree_bp.route("/trees/<int:tree_id>", methods=["GET"])
def get_tree(tree_id):
    tree = Tree.query.get(tree_id)
    if not tree:
        return fail("Tree not found.", 404)
    return ok("Tree fetched.", tree.to_dict())


@tree_bp.route("/trees", methods=["POST"])
@optional_auth
def create_tree():
    """Register a newly planted tree (used by plantation / volunteer flows)."""
    try:
        body = request.get_json(silent=True) or {}
        tree = Tree(
            species=body.get("species", "Neem"),
            common_name=body.get("common_name", ""),
            latitude=body.get("latitude", 21.7645),
            longitude=body.get("longitude", 72.1519),
            location_name=body.get("location_name", "Bhavnagar"),
            health_status=body.get("health_status", "healthy"),
            height_m=body.get("height_m", 1.2),
            forest_site_id=body.get("forest_site_id"),
            image_url=body.get("image_url", ""),
        )
        db.session.add(tree)
        db.session.commit()
        return ok("Tree registered successfully.", tree.to_dict(), 201)
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not register tree: {exc}", 500)


@tree_bp.route("/trees/<int:tree_id>/adopt", methods=["POST"])
@token_required
def adopt_tree(tree_id):
    """Backs useAdoptTree()."""
    try:
        tree = Tree.query.get(tree_id)
        if not tree:
            return fail("Tree not found.", 404)
        if tree.adopted_by_user_id:
            return fail("This tree has already been adopted.", 409)

        tree.adopted_by_user_id = g.current_user["user_id"]
        tree.adopted_at = datetime.utcnow()
        db.session.commit()
        return ok("Tree adopted successfully!", tree.to_dict())
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not adopt tree: {exc}", 500)
