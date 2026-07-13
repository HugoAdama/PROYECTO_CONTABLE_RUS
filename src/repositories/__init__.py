# src/repositories/__init__.py
from .base_repository import BaseRepository
from .factura_repository import FacturaRepository
from .boleta_repository import BoletaRepository
from .percepcion_repository import PercepcionRepository

__all__ = ['BaseRepository', 'FacturaRepository', 'BoletaRepository', 'PercepcionRepository']