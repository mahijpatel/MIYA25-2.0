from datetime import datetime

from models import db, SerializerMixin


class SensorReading(db.Model, SerializerMixin):
    __tablename__ = "sensor_readings"

    id = db.Column(db.Integer, primary_key=True)
    sensor_code = db.Column(db.String(40), nullable=False)
    sensor_type = db.Column(db.String(30), default="soil-moisture")  # soil-moisture | temperature | humidity | aqi
    forest_site_id = db.Column(db.Integer, db.ForeignKey("forest_sites.id"), nullable=True)
    value = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(20), default="%")
    battery_percent = db.Column(db.Float, default=90.0)
    status = db.Column(db.String(20), default="online")  # online | offline | low-battery
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
