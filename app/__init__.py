# app/__init__.py
# ===============

import os
import logging
from pathlib import Path
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool  # <--- IMPORTANTE: Importar la clase

# Cargar variables de entorno
load_dotenv()

# Importar base de datos
from src.database.conexion import db
from src.database.models import Documento, Configuracion, Historial


def create_app(config_name: str = 'development') -> Flask:
    """Fábrica de aplicación Flask."""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')
    
    # ==========================================
    # CONFIGURACIÓN DIRECTA DE LA BASE DE DATOS
    # ==========================================
    
    # Obtener ruta base del proyecto
    base_dir = Path(__file__).parent.parent.absolute()
    
    # Crear directorio data si no existe
    data_dir = base_dir / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Ruta de la base de datos
    db_path = data_dir / 'rus.db'
    db_uri = f'sqlite:///{db_path}'
    
    # Configurar SQLAlchemy DIRECTAMENTE en app.config
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'poolclass': StaticPool,  # <--- USAR LA CLASE, no el string
        'connect_args': {'check_same_thread': False}
    }
    
       # ==========================================
    # OTRAS CONFIGURACIONES
    # ==========================================

    secret_key = os.getenv("SECRET_KEY")
    app_env = os.getenv("APP_ENV", "development").lower()

    if app_env == "production" and not secret_key:
        raise RuntimeError(
            "SECRET_KEY no está configurada. Defínela en las variables de entorno."
        )

    if not secret_key:
        app.logger.warning(
            "SECRET_KEY no encontrada. Usando clave temporal para desarrollo."
        )
        secret_key = os.urandom(32).hex()

    app.config["SECRET_KEY"] = secret_key

    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    app.config["UPLOAD_FOLDER"] = data_dir / "uploads"
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    # Límites RUS
    app.config['LIMITE_RUS'] = int(os.getenv('LIMITE_RUS', 8000))
    app.config['IMPUESTO_NORMAL'] = float(os.getenv('IMPUESTO_NORMAL', 20.00))
    app.config['IMPUESTO_ALERTA'] = float(os.getenv('IMPUESTO_ALERTA', 50.00))
    
    # ==========================================
    # INICIALIZAR BASE DE DATOS
    # ==========================================
    
    # Inicializar db con la app
    db.init_app(app)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
        app.logger.info(f"✅ Base de datos inicializada en: {db_path}")
        
        # Configuración inicial
        try:
            if not Configuracion.query.first():
                app.logger.info("Creando configuración por defecto...")
                default_configs = [
                    ('color_primario', '#4A90D9'),
                    ('nombre_negocio', 'Maria Boutique'),
                    ('limite_rus', '8000'),
                    ('impuesto_normal', '20'),
                    ('impuesto_alerta', '50'),
                ]
                for key, value in default_configs:
                    Configuracion.set(key, value)
                app.logger.info("✅ Configuración por defecto creada")
        except Exception as e:
            app.logger.error(f"Error al crear configuración: {e}")
    
    # ==========================================
    # REGISTRAR BLUEPRINTS Y OTROS
    # ==========================================
    
    _register_blueprints(app)
    _setup_logging(app)
    _register_cli_commands(app)
    _register_template_filters(app)
    
    return app


def _register_blueprints(app: Flask) -> None:
    """Registra los blueprints."""
    from app.routes import main_bp
    app.register_blueprint(main_bp)


def _setup_logging(app: Flask) -> None:
    """Configura el logging."""
    if not app.debug:
        log_dir = Path('logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / 'app.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
        app.logger.addHandler(file_handler)
    
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


def _register_cli_commands(app: Flask) -> None:
    """Registra comandos CLI."""
    import click
    
    @app.cli.command('init-db')
    def init_db_command():
        """Inicializa la base de datos."""
        with app.app_context():
            db.create_all()
            click.echo('✅ Base de datos inicializada correctamente.')


def _register_template_filters(app: Flask) -> None:
    """Registra filtros de template."""
    @app.template_filter('currency')
    def currency_filter(value):
        if value is None:
            return 'S/ 0.00'
        return f'S/ {float(value):.2f}'
    
    @app.template_filter('percentage')
    def percentage_filter(value):
        if value is None:
            return '0%'
        sign = '+' if value >= 0 else ''
        return f'{sign}{float(value):.1f}%'
