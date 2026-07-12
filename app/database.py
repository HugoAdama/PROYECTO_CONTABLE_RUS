# app/database.py
"""
🗄️ CONEXIÓN A BASE DE DATOS
Configuración de SQLite para Flask
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pathlib import Path
import os

# Ruta de la base de datos
DB_PATH = Path(__file__).parent.parent / "contable.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Crear engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sesión por request
def get_db():
    """Obtiene una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()