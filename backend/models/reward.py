from datetime import datetime

from models import db, SerializerMixin


class Reward(db.Model, SerializerMixin):
    """A redeemable reward in the catalog."""

    __tablename__ = "rewards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    cost_points = db.Column(db.Integer, default=100)
    category = db.Column(db.String(60), default="voucher")
    stock = db.Column(db.Integer, default=50)
    image_url = db.Column(db.String(255), default="")
    is_active = db.Column(db.Boolean, default=True)


class Badge(db.Model, SerializerMixin):
    """A badge definition (catalog)."""

    __tablename__ = "badges"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    icon = db.Column(db.String(60), default="badge")
    points_required = db.Column(db.Integer, default=100)


class UserBadge(db.Model, SerializerMixin):
    __tablename__ = "user_badges"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey("badges.id"), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)


class RedemptionHistory(db.Model, SerializerMixin):
    __tablename__ = "redemption_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey("rewards.id"), nullable=False)
    points_spent = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="completed")  # pending | completed | cancelled
    redeemed_at = db.Column(db.DateTime, default=datetime.utcnow)
