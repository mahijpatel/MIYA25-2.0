from datetime import datetime

from models import db, SerializerMixin


class ForestSite(db.Model, SerializerMixin):
    __tablename__ = "forest_sites"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    latitude = db.Column(db.Float, default=21.7645)
    longitude = db.Column(db.Float, default=72.1519)
    area_hectares = db.Column(db.Float, default=5.0)
    tree_count = db.Column(db.Integer, default=0)
    canopy_cover_percent = db.Column(db.Float, default=40.0)
    status = db.Column(db.String(30), default="active")  # active | degraded | restored
    description = db.Column(db.Text, default="")
    image_url = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
