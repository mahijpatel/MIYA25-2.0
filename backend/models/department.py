from models import db, SerializerMixin


class Department(db.Model, SerializerMixin):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    head_name = db.Column(db.String(120), default="")
    contact_email = db.Column(db.String(150), default="")
    contact_phone = db.Column(db.String(30), default="")
    staff_count = db.Column(db.Integer, default=10)
    budget_inr = db.Column(db.Float, default=1000000.0)
    description = db.Column(db.Text, default="")
