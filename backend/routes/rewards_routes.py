from datetime import datetime

from flask import Blueprint, g, request

from models import db
from models.reward import Badge, RedemptionHistory, Reward, UserBadge
from models.user import User
from utils.decorators import optional_auth, token_required
from utils.response import fail, ok

rewards_bp = Blueprint("rewards", __name__, url_prefix="/api")


@rewards_bp.route("/rewards", methods=["GET"])
def list_rewards():
    """GET /rewards - the redeemable catalog."""
    rewards = Reward.query.filter_by(is_active=True).order_by(Reward.cost_points).all()
    return ok("Rewards fetched.", [r.to_dict() for r in rewards])


@rewards_bp.route("/badges", methods=["GET"])
@optional_auth
def list_badges():
    """GET /badges - all badge definitions, flagged if the current user earned them."""
    badges = Badge.query.order_by(Badge.points_required).all()
    user = g.get("current_user")
    earned_ids = set()
    if user:
        earned_ids = {ub.badge_id for ub in UserBadge.query.filter_by(user_id=user["user_id"]).all()}

    result = []
    for b in badges:
        data = b.to_dict()
        data["earned"] = b.id in earned_ids
        result.append(data)
    return ok("Badges fetched.", result)


@rewards_bp.route("/wallet", methods=["GET"])
@token_required
def get_wallet():
    """GET /wallet - the current user's points balance."""
    user = User.query.get(g.current_user["user_id"])
    if not user:
        return fail("User not found.", 404)

    spent = (
        db.session.query(db.func.coalesce(db.func.sum(RedemptionHistory.points_spent), 0))
        .filter(RedemptionHistory.user_id == user.id, RedemptionHistory.status != "cancelled")
        .scalar()
    )
    return ok(
        "Wallet fetched.",
        {
            "user_id": user.id,
            "balance_points": user.points,
            "lifetime_points_spent": int(spent or 0),
            "level": user.level,
        },
    )


@rewards_bp.route("/history", methods=["GET"])
@token_required
def get_history():
    """GET /history - redemption history for the current user."""
    records = (
        RedemptionHistory.query.filter_by(user_id=g.current_user["user_id"])
        .order_by(RedemptionHistory.redeemed_at.desc())
        .all()
    )
    return ok("Redemption history fetched.", [r.to_dict() for r in records])


@rewards_bp.route("/redeem", methods=["POST"])
@token_required
def redeem_reward():
    """POST /redeem - spend points on a catalog reward."""
    try:
        body = request.get_json(silent=True) or {}
        reward_id = body.get("reward_id")
        reward = Reward.query.get(reward_id) if reward_id else None
        if not reward or not reward.is_active:
            return fail("Reward not found or no longer available.", 404)

        if reward.stock <= 0:
            return fail("This reward is out of stock.", 409)

        user = User.query.get(g.current_user["user_id"])
        if not user:
            return fail("User not found.", 404)

        if user.points < reward.cost_points:
            return fail("You don't have enough points for this reward.", 400)

        user.points -= reward.cost_points
        reward.stock -= 1

        history = RedemptionHistory(
            user_id=user.id,
            reward_id=reward.id,
            points_spent=reward.cost_points,
            status="completed",
            redeemed_at=datetime.utcnow(),
        )
        db.session.add(history)
        db.session.commit()

        return ok(
            "Reward redeemed successfully!",
            {"wallet_balance": user.points, "redemption": history.to_dict()},
            201,
        )
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        return fail(f"Could not redeem reward: {exc}", 500)
