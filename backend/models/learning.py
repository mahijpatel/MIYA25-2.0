from models import db, SerializerMixin


class LearningArticle(db.Model, SerializerMixin):
    __tablename__ = "learning_articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(60), default="general")
    summary = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    read_minutes = db.Column(db.Integer, default=4)
    image_url = db.Column(db.String(255), default="")
