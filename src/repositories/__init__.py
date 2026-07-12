# src/repositories/__init__.py
"""
📁 REPOSITORIOS - PUNTO DE ENTRADA
Exporta todas las clases de repositorios para facilitar su uso
"""

from .base_repository import BaseRepository
from .factura_repository import FacturaRepository
from .boleta_repository import BoletaRepository
from .percepcion_repository import PercepcionRepository

__all__ = [
    'BaseRepository',
    'FacturaRepository',
    'BoletaRepository',
    'PercepcionRepository'
]