from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import structlog
from app.logging_config import configure_logging

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configurar logging
    configure_logging()
    
    # Configuración de la base de datos (SQLite en este caso)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de rate limiting
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"]
    )
    
    return app