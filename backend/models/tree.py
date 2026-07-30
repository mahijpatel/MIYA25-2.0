from datetime import datetime

from models import db, SerializerMixin


class Tree(db.Model, SerializerMixin):
    __tablename__ = "trees"

    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(120), nullable=False)
    common_name = db.Column(db.String(120), default="")
    latitude = db.Column(db.Float, default=21.7645)
    longitude = db.Column(db.Float, default=72.1519)
    location_name = db.Column(db.String(160), default="Bhavnagar")
    health_status = db.Column(db.String(30), default="healthy")  # healthy | stressed | diseased | dead
    height_m = db.Column(db.Float, default=1.5)
    age_years = db.Column(db.Float, default=1.0)
    co2_absorbed_kg = db.Column(db.Float, default=12.0)
    planted_on = db.Column(db.DateTime, default=datetime.utcnow)
    forest_site_id = db.Column(db.Integer, db.ForeignKey("forest_sites.id"), nullable=True)
    adopted_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    adopted_at = db.Column(db.DateTime, nullable=True)
    image_url = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
