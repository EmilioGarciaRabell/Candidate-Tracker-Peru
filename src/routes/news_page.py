from flask import Blueprint, jsonify
from src.services.data_management import news

news_bp = Blueprint('page_bp', __name__)

@news_bp.route("/api/news/<string:batch>", methods=["GET"])
# @page_bp.route("/api/news/<string:batch>/<int:candidate_id>", methods=["GET"])
def get_news(batch):
    n = news.get_candidate_news(batch)
    return jsonify({'news':n}) , 200

