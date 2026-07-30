from datetime import datetime

from models import db, SerializerMixin


class DroneMission(db.Model, SerializerMixin):
    __tablename__ = "drone_missions"

    id = db.Column(db.Integer, primary_key=True)
    mission_name = db.Column(db.String(160), nullable=False)
    forest_site_id = db.Column(db.Integer, db.ForeignKey("forest_sites.id"), nullable=True)
    pilot_name = db.Column(db.String(120), default="Unassigned")
    status = db.Column(db.String(20), default="scheduled")  # scheduled | in-flight | completed | aborted
    area_covered_hectares = db.Column(db.Float, default=10.0)
    findings = db.Column(db.Text, default="")
    scheduled_at = db.Column(db.DateTime, default=datetime.utcnow)
