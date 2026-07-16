"""Blueprint principal de la interfaz web y API de Contable RUS."""

from flask import Blueprint

main_bp = Blueprint("main", __name__)

# Importar módulos después de crear el Blueprint para registrar sus rutas.
from contable.api import (  # noqa: E402,F401
    carpetas,
    configuracion,
    dashboard,
    documentos,
    exportar,
    reportes,
)

__all__ = ["main_bp"]
