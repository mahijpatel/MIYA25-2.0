from flask import Blueprint, request

from models.user import User
from utils.response import ok

leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/api")


@leaderboard_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    """Backs useLeaderboard(). Ranks citizens by points."""
    limit = request.args.get("limit", default=20, type=int)
    users = (
        User.query.filter_by(role="citizen", is_active=True)
        .order_by(User.points.desc())
        .limit(limit)
        .all()
    )
    ranked = []
    for index, user in enumerate(users, start=1):
        ranked.append(
            {
                "rank": index,
                "user_id": user.id,
                "name": user.name,
                "avatar_url": user.avatar_url,
                "points": user.points,
                "level": user.level,
                "city": user.city,
            }
        )
    return ok("Leaderboard fetched.", ranked)
