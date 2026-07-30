from models import db, SerializerMixin


class HeatZone(db.Model, SerializerMixin):
    __tablename__ = "heat_zones"

    id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(160), nullable=False)
    latitude = db.Column(db.Float, default=21.7645)
    longitude = db.Column(db.Float, default=72.1519)
    surface_temp_c = db.Column(db.Float, default=38.0)
    heat_risk = db.Column(db.String(20), default="moderate")  # low | moderate | high | extreme
    green_cover_percent = db.Column(db.Float, default=15.0)
