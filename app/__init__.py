# app/__init__.py
"""
Fábrica de la aplicación Flask
"""

from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123456')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    # Registrar blueprint
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app