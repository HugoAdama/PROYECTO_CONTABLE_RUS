"""
Repositorios - Punto de entrada
"""
from .factura_repository import FacturaRepository
from .boleta_repository import BoletaRepository
from .percepcion_repository import PercepcionRepository

__all__ = [
    'FacturaRepository',
    'BoletaRepository',
    'PercepcionRepository'
]