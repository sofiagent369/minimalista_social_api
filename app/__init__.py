from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuración de la base de datos (SQLite en este caso)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    return app