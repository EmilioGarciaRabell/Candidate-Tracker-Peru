from flask import Blueprint, jsonify
from src.services.data_management import news
from etl.news_features.get_latest_news import call_api_store_initial_news

news_bp = Blueprint('page_bp', __name__)


def run_morning_batch():
    print("Running morning batch...")
    call_api_store_initial_news()
    news.store_candidates_news("morning")
    print("Morning batch done")

def run_evening_batch():
    print("Running evening batch...")
    call_api_store_initial_news()
    news.store_candidates_news("evening")
    print("Evening batch done")

 

@news_bp.route("/api/news", methods=["GET"])
def get_candidate_news():
    n = news.get_news()
    if not n:
        return jsonify({"news": []})
    return jsonify(n[0]["news_json"])
    




