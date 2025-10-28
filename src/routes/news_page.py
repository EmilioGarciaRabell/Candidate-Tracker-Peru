from flask import Blueprint, jsonify
from src.services.data_management import news
from etl.get_latest_news import store_news
from flask_apscheduler import APScheduler

news_bp = Blueprint('page_bp', __name__)
scheduler = APScheduler()


def run_morning_batch():
    print("Running morning batch...")
    store_news()
    news.store_candidates_news("morning")
    print("Morning batch done")

def run_evening_batch():
    print("Running evening batch...")
    store_news()
    news.store_candidates_news("evening")
    print("Evening batch done")

##get the news api and store them in the database
scheduler.add_job(id='my_job', func=run_morning_batch, trigger='cron', hour=8, minute=0)
scheduler.add_job(id='my_job', func=run_evening_batch, trigger='cron', hour=19, minute=0)

@news_bp.route("/api/news/<string:batch>", methods=["GET"])
# @page_bp.route("/api/news/<string:batch>/<int:candidate_id>", methods=["GET"])
def get_candidate_news(batch):
    n = news.get_news(batch)
    return n,200

    




