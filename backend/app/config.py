import os
from dotenv import load_dotenv

# Load environmental variables from .env file if it exists
load_dotenv()

class Config:
    """Base Configuration Class"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', '0b44ca19022clea18bb659b30fdf133a0fbc822f115c59cc64c58f2ccb8c71a5')
    
    # Session configurations
    SESSION_PERMANENT = True
    
    # Database configurations (MySQL)
    MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
    MYSQL_USER = os.getenv('DB_USER', 'root')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'Juneoct@9')
    MYSQL_DB = os.getenv('DB_NAME', 'shopping_db')
    
    # AI/ML Configuration
    MAX_RECOMMENDATIONS = int(os.getenv('MAX_RECOMMENDATIONS', '5'))
    
    # Debug mode flag
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
