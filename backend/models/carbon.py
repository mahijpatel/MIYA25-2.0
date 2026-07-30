from datetime import datetime

from models import db, SerializerMixin


class CarbonLog(db.Model, SerializerMixin):
    __tablename__ = "carbon_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    transport_kg = db.Column(db.Float, default=0.0)
    electricity_kg = db.Column(db.Float, default=0.0)
    diet_kg = db.Column(db.Float, default=0.0)
    waste_kg = db.Column(db.Float, default=0.0)
    total_kg = db.Column(db.Float, default=0.0)
    diet_type = db.Column(db.String(20), default="mixed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
