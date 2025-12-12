from flask import Flask, jsonify
from src.config import Config
from src.extensions import  cors, limiter

from src.routes.main_routes import main_bp
from src.routes.candidate_page import candidate_bp
from src.routes.news_page import news_bp
from src.routes.google_cloud_storage import google_storage_bp
from src.routes.parties_routes import PARTY
from src.routes.comparison_tool import comparison_bp
from src.routes.contact_page import contact_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    cors.init_app(
        app,
        resources={r"/*": {"origins": app.config["FRONTEND_ORIGINS"]}}
    )

    # rate limiter
    limiter.init_app(app)

    # Initialize extensions
    cors.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(google_storage_bp)
    app.register_blueprint(PARTY)
    app.register_blueprint(comparison_bp)
    app.register_blueprint(contact_bp)
 

        # ---- Error Handlers ----
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def handle_500(e):
        # You can log e here
        return jsonify({"error": "Internal server error"}), 500

    # Rate-limiter error (HTTP 429)
    @app.errorhandler(429)
    def handle_429(e):
        return (
            jsonify(
                {
                    "error": "Too many requests",
                    "message": "You have exceeded the allowed number of requests. Please try again later.",
                }
            ),
            429,
        )


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"])

