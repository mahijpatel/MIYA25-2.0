from models import db, SerializerMixin


class FloodZone(db.Model, SerializerMixin):
    __tablename__ = "flood_zones"

    id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(160), nullable=False)
    latitude = db.Column(db.Float, default=21.7645)
    longitude = db.Column(db.Float, default=72.1519)
    risk_level = db.Column(db.String(20), default="moderate")  # low | moderate | high | severe
    water_level_m = db.Column(db.Float, default=0.5)
    population_at_risk = db.Column(db.Integer, default=100)
    last_updated = db.Column(db.String(60), default="")
