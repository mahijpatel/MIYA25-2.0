from datetime import datetime

from models import db, SerializerMixin


class Volunteer(db.Model, SerializerMixin):
    """A volunteering opportunity/event (not a person)."""

    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    organizer = db.Column(db.String(160), default="MIYA25 Bhavnagar")
    location_name = db.Column(db.String(160), default="Bhavnagar")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    slots_total = db.Column(db.Integer, default=20)
    slots_filled = db.Column(db.Integer, default=0)
    category = db.Column(db.String(60), default="tree-plantation")
    description = db.Column(db.Text, default="")


class VolunteerSignup(db.Model, SerializerMixin):
    __tablename__ = "volunteer_signups"

    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    full_name = db.Column(db.String(120), default="")
    phone = db.Column(db.String(20), default="")
    status = db.Column(db.String(20), default="confirmed")  # confirmed | waitlisted | cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
