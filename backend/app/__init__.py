from flask import Flask, g
from flask_bcrypt import Bcrypt
from app.config import Config
from app.services.db import DatabaseService
from app.services.recommender import RecommendationService
from app.services.sentiment import SentimentService

# Instantiate global Bcrypt extension
bcrypt = Bcrypt()

def create_app(config_class=Config) -> Flask:
    """
    Application Factory pattern to compile the Flask app modularly.
    Initializes extensions, injects services, and registers routers.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask Extensions
    bcrypt.init_app(app)

    # Register application teardown context hook to close connections cleanly
    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db_conn', None)
        if db is not None:
            try:
                db.close()
            except Exception:
                pass

    # Instantiate services inside the app context
    with app.app_context():
        # Core DB layer service using pure PyMySQL
        db_service = DatabaseService()
        
        # AI/ML services
        recommender_service = RecommendationService(db_service)
        sentiment_service = SentimentService()

        # Import routing Blueprints
        from app.routes.auth import auth_bp, init_auth
        from app.routes.products import products_bp, init_products
        from app.routes.ai import ai_bp, init_ai

        # Inject services into routes (Dependency Injection pattern)
        init_auth(db_service)
        init_products(db_service, recommender_service, sentiment_service)
        init_ai(db_service)

        # Register Blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(products_bp)
        app.register_blueprint(ai_bp)

    return app
