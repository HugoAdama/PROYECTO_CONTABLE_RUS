"""
Conexión a la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Configuración de la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///instance/contable.db')

def get_db():
    """Obtiene una sesión de base de datos."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_engine():
    """Obtiene el motor de la base de datos."""
    return create_engine(DATABASE_URL)
