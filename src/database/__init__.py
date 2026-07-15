# src/database/__init__.py
# ========================
# Módulo de base de datos

from .conexion import db, db_manager
from .models import Documento, Configuracion, Historial

# Funciones de compatibilidad (mantener para código existente)
def get_db():
    """Retorna la instancia de SQLAlchemy."""
    return db

def init_db(app):
    """Inicializa la base de datos (compatibilidad)."""
    db.init_app(app)

__all__ = [
    'db',
    'db_manager',
    'get_db',
    'init_db',
    'Documento',
    'Configuracion',
    'Historial'
]
