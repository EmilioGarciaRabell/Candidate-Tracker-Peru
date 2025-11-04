from flask import Flask
from src.config import Config
from src.extensions import  cors
from src.routes.main_routes import main_bp
from src.routes.candidate_page import candidate_bp
from src.routes.news_page import news_bp, run_morning_batch, run_evening_batch
from flask_apscheduler import APScheduler
from datetime import timezone
import pytz


scheduler = APScheduler()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    cors.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(news_bp)

    ##start scheduler
    scheduler.init_app(app)
    scheduler.start()
    print("Scheduler started")

    ##schedule to get news in morning and evening
    scheduler.add_job(id='morning', func=run_morning_batch, trigger='cron', hour=8, minute=0)
    scheduler.add_job(id='evening', func=run_evening_batch, trigger='cron', hour=21, minute=10,timezone=pytz.timezone('America/New_York'))

    for job in scheduler.get_jobs():
        print(f"Job '{job.id}' next run: {job.next_run_time}")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
