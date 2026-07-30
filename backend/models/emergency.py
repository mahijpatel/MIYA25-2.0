from datetime import datetime

from models import db, SerializerMixin


class EmergencyReport(db.Model, SerializerMixin):
    __tablename__ = "emergency_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    category = db.Column(db.String(40), default="fire")  # fire | flood | illegal-cutting | wildlife | other
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    latitude = db.Column(db.Float, default=21.7645)
    longitude = db.Column(db.Float, default=72.1519)
    location_name = db.Column(db.String(160), default="Bhavnagar")
    severity = db.Column(db.String(20), default="medium")  # low | medium | high | critical
    status = db.Column(db.String(20), default="reported")  # reported | acknowledged | in-progress | resolved
    attachment_filename = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
