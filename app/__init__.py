from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# ============================================
# db a nivel de módulo - ACCESIBLE PARA TODA LA APP
# ============================================
db = SQLAlchemy()

def create_app():
    """Fábrica de la aplicación Flask"""
    load_dotenv()
    app = Flask(__name__)
    
    # Configuraciones
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.getenv('DB_NAME', 'contable.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'data/pdfs')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 52428800))
    
    # Inicializar db con la app
    db.init_app(app)
    
    # Crear tablas si no existen
    with app.app_context():
        from src.database import crear_tablas
        crear_tablas()
    
    # Registrar rutas
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app