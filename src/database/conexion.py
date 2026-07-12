# src/database/conexion.py
"""
Módulo de conexión a la base de datos SQLite
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

# ============================================================
# BASE PARA MODELOS
# ============================================================

Base = declarative_base()


class DatabaseConnection:
    """Singleton para manejar la conexión a la base de datos"""
    
    _instance = None
    _engine = None
    _session_factory = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def _inicializar(self):
        """Inicializa la conexión a la base de datos"""
        if self._initialized:
            return
            
        # Ruta a la base de datos
        db_path = Path(__file__).parent.parent.parent / 'contable.db'
        
        # Crear engine
        self._engine = create_engine(
            f'sqlite:///{db_path}',
            echo=False,
            connect_args={'check_same_thread': False}
        )
        
        # Crear session factory
        self._session_factory = sessionmaker(bind=self._engine)
        self._initialized = True
    
    def create_all_tables(self):
        """Crea todas las tablas definidas en los modelos"""
        self._inicializar()
        # Importar modelos aquí para asegurar que estén registrados
        from src.models.factura_compra import FacturaCompra
        from src.models.boleta_venta import BoletaVenta
        from src.models.percepcion import Percepcion
        
        Base.metadata.create_all(self._engine)
        print("✅ Tablas creadas exitosamente")
    
    def get_session(self):
        """Obtiene una sesión de base de datos"""
        self._inicializar()
        return self._session_factory()
    
    def get_engine(self):
        """Obtiene el engine de la base de datos"""
        self._inicializar()
        return self._engine
    
    def close(self):
        """Cierra la conexión"""
        if self._engine:
            self._engine.dispose()


# ============================================================
# FUNCIONES DE CONVENIENCIA
# ============================================================

def get_db():
    """Obtiene una sesión de base de datos"""
    return DatabaseConnection().get_session()


def get_session():
    """Obtiene una sesión de base de datos (alias)"""
    return DatabaseConnection().get_session()


def get_engine():
    """Obtiene el engine de la base de datos"""
    return DatabaseConnection().get_engine()


def init_db():
    """Inicializa la base de datos y crea todas las tablas"""
    db = DatabaseConnection()
    db.create_all_tables()
    return db


def close_db():
    """Cierra la conexión a la base de datos"""
    DatabaseConnection().close()


# ============================================================
# COMPATIBILIDAD CON REPOSITORIOS
# ============================================================

# Alias para compatibilidad con código existente
SessionLocal = sessionmaker(bind=DatabaseConnection().get_engine())