# src/database/conexion.py
# ========================
# Conexión a base de datos - Versión simplificada

import logging
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session

logger = logging.getLogger(__name__)

# Instancia global de SQLAlchemy
db = SQLAlchemy()


class DatabaseManager:
    """Gestor de base de datos simplificado."""
    
    def __init__(self):
        self._engine = None
        self._scoped_session = None
    
    def init_app(self, app):
        """Inicializa con la aplicación Flask."""
        # db ya está inicializado con la app en app/__init__.py
        self._engine = db.engine
        self._scoped_session = scoped_session(sessionmaker(bind=self._engine))
        logger.info("DatabaseManager inicializado")
    
    @contextmanager
    def session(self):
        """Context manager para sesiones."""
        session = self._scoped_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error en sesión: {e}")
            raise
        finally:
            session.close()
    
    def get_engine(self):
        return self._engine


# Instancia global
db_manager = DatabaseManager()


# ==========================================
# FUNCIONES DE COMPATIBILIDAD
# ==========================================

def get_db():
    """Retorna la instancia de SQLAlchemy."""
    return db


def init_db(app):
    """Inicializa la base de datos (compatibilidad)."""
    db.init_app(app)
    # También inicializar db_manager
    db_manager.init_app(app)
