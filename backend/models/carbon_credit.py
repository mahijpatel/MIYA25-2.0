from datetime import datetime

from models import db, SerializerMixin


class CarbonCredit(db.Model, SerializerMixin):
    __tablename__ = "carbon_credits"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(160), nullable=False)
    forest_site_id = db.Column(db.Integer, db.ForeignKey("forest_sites.id"), nullable=True)
    credits_issued = db.Column(db.Float, default=0.0)
    credits_sold = db.Column(db.Float, default=0.0)
    price_per_credit_inr = db.Column(db.Float, default=850.0)
    status = db.Column(db.String(30), default="verified")  # pending | verified | sold
    issued_on = db.Column(db.DateTime, default=datetime.utcnow)
