from datetime import datetime

from models import db, SerializerMixin


class Pickup(db.Model, SerializerMixin):
    __tablename__ = "pickups"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    waste_type = db.Column(db.String(40), default="organic")  # organic | recyclable | e-waste
    quantity_kg = db.Column(db.Float, default=1.0)
    address = db.Column(db.String(200), default="Bhavnagar")
    scheduled_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="scheduled")  # scheduled | collected | cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
