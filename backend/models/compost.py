from datetime import datetime

from models import db, SerializerMixin


class CompostUnit(db.Model, SerializerMixin):
    __tablename__ = "compost_units"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    location_name = db.Column(db.String(160), default="Bhavnagar")
    latitude = db.Column(db.Float, default=21.7645)
    longitude = db.Column(db.Float, default=72.1519)
    capacity_kg = db.Column(db.Float, default=500.0)
    current_load_kg = db.Column(db.Float, default=120.0)
    status = db.Column(db.String(20), default="operational")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
