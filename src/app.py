from flask import Flask
from src.config import Config
from src.extensions import  cors
from src.routes.main_routes import main_bp
from src.routes.candidate_page import candidate_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    cors.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(candidate_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
