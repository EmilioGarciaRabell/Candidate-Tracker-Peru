from flask import Flask
from src.config import Config
from src.extensions import  cors
from src.routes.main_routes import main_bp
from src.routes.candidate_page import candidate_bp
from src.routes.google_cloud_storage import google_storage_bp
from src.routes.parties_routes import PARTY

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    cors.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(google_storage_bp)
    app.register_blueprint(PARTY)

    for rule in app.url_map.iter_rules():
        print(rule, rule.endpoint)
    return app

if __name__ == "__main__":
    
    app = create_app()
    app.run()
