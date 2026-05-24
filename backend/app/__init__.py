import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from app.config import Config
from app.services.db import DatabaseService
from app.services.recommender import RecommendationService
from app.services.sentiment import SentimentService

# Instantiate global Flask-MySQLdb and Bcrypt extensions
mysql = MySQL()
bcrypt = Bcrypt()

def create_app(config_class=Config) -> Flask:
    """
    Application Factory pattern to compile the Flask app modularly.
    Initializes extensions, injects services, and registers routers.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask Extensions
    mysql.init_app(app)
    bcrypt.init_app(app)

    # Instantiate services inside the app context
    with app.app_context():
        # Core DB layer service
        db_service = DatabaseService(mysql)
        
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
