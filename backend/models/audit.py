from datetime import datetime

from models import db, SerializerMixin


class AuditLog(db.Model, SerializerMixin):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    actor_name = db.Column(db.String(120), default="system")
    action = db.Column(db.String(160), nullable=False)
    resource = db.Column(db.String(120), default="")
    ip_address = db.Column(db.String(60), default="127.0.0.1")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
