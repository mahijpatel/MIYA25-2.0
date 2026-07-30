from datetime import datetime

from models import db, SerializerMixin


class Feedback(db.Model, SerializerMixin):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    subject = db.Column(db.String(160), default="General Feedback")
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
