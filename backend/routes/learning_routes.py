from flask import Blueprint, request

from models.learning import LearningArticle
from utils.response import ok

learning_bp = Blueprint("learning", __name__, url_prefix="/api")


@learning_bp.route("/learning-articles", methods=["GET"])
def list_learning_articles():
    """Backs useLearningArticles()."""
    query = LearningArticle.query
    category = request.args.get("category")
    if category:
        query = query.filter_by(category=category)
    articles = query.order_by(LearningArticle.id).all()
    return ok("Learning articles fetched.", [a.to_dict() for a in articles])
