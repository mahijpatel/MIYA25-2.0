from flask import Blueprint, g

from models.achievement import Achievement, UserAchievement
from utils.decorators import optional_auth
from utils.response import ok

achievement_bp = Blueprint("achievements", __name__, url_prefix="/api")


@achievement_bp.route("/achievements", methods=["GET"])
@optional_auth
def list_achievements():
    """Backs useAchievements(). Shows every achievement plus whether the
    current user has unlocked it."""
    achievements = Achievement.query.order_by(Achievement.id).all()
    user = g.get("current_user")
    unlocked_ids = set()
    if user:
        unlocked_ids = {
            ua.achievement_id
            for ua in UserAchievement.query.filter_by(user_id=user["user_id"]).all()
        }

    result = []
    for a in achievements:
        data = a.to_dict()
        data["unlocked"] = a.id in unlocked_ids
        result.append(data)
    return ok("Achievements fetched.", result)
