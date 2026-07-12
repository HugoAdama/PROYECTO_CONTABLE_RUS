# src/database/conexion.py
"""
🗄️ CONEXIÓN A BASE DE DATOS
Configuración y gestión de la conexión SQLite
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# URL de la base de datos
DATABASE_URL = f"sqlite:///./{os.getenv('DB_NAME', 'contable.db')}"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Cambiar a True para ver SQL en consola
)

# Crear sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para modelos
Base = declarative_base()

def get_db():
    """
    Generador de sesiones para usar con dependencias.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()