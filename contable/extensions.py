"""
Extensiones Flask compartidas por Contable RUS.

Durante la migración, la nueva arquitectura reutiliza la instancia legacy
de SQLAlchemy para mantener una única instancia activa.
"""

from src.database.conexion import db


__all__ = ["db"]
