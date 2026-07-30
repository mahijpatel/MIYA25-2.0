from datetime import datetime

from models import db, SerializerMixin


class Complaint(db.Model, SerializerMixin):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    category = db.Column(db.String(60), default="tree-damage")
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    location_name = db.Column(db.String(160), default="Bhavnagar")
    latitude = db.Column(db.Float, default=21.7645)
    longitude = db.Column(db.Float, default=72.1519)
    attachment_filename = db.Column(db.String(255), default="")
    status = db.Column(db.String(20), default="submitted")  # submitted | under-review | resolved | rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
