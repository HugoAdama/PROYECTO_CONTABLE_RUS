# src/extractors/__init__.py
# ===========================
# Módulo de extractores para diferentes tipos de documentos

from .base import BaseExtractor
from .factura_natura import FacturaNaturaExtractor
from .boleta import BoletaExtractor
from .percepcion import PercepcionExtractor

__all__ = [
    'BaseExtractor',
    'FacturaNaturaExtractor',
    'BoletaExtractor',
    'PercepcionExtractor'
]
