from flask import Blueprint, jsonify
from src.services.data_management import news

news_bp = Blueprint('page_bp', __name__)




 

@news_bp.route("/api/news", methods=["GET"])
def get_candidate_news():
    n = news.get_news()
    if not n:
        return jsonify({"news": []})
    return jsonify(n)
    




