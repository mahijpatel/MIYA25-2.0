from datetime import datetime

from models import db, SerializerMixin


class Achievement(db.Model, SerializerMixin):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    icon = db.Column(db.String(60), default="award")
    points_reward = db.Column(db.Integer, default=50)
    category = db.Column(db.String(60), default="general")


class UserAchievement(db.Model, SerializerMixin):
    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievements.id"), nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
