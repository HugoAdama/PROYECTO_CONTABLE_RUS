# app/__init__.py
"""
📊 APLICACIÓN FLASK
Configuración principal
"""

from flask import Flask
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent))

# Cargar variables de entorno
load_dotenv()

def create_app():
    """Crea y configura la aplicación Flask."""
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # ← AÑADIR ESTO
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # ← AÑADIR ESTO
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'data/pdfs')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
    
    # Registrar rutas
    from app.routes import register_routes
    register_routes(app)
    
    return app