from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from models import db, SerializerMixin


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="citizen")  # citizen | gov | admin
    phone = db.Column(db.String(20), default="")
    city = db.Column(db.String(80), default="Bhavnagar")
    avatar_url = db.Column(db.String(255), default="")
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.String(40), default="Seedling")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def to_public_dict(self):
        data = self.to_dict()
        data.pop("password_hash", None)
        return data
