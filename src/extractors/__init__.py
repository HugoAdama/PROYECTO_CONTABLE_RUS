"""
EXTRACTORES - PUNTO DE ENTRADA
Exporta todos los extractores para facilitar su uso
"""
from .base_extractor import BaseExtractor
from .detector_extractor import DetectorExtractor
from .factura_extractor import FacturaExtractor
from .boleta_extractor import BoletaExtractor
from .percepcion_extractor import PercepcionExtractor

__all__ = [
    'BaseExtractor',
    'DetectorExtractor',
    'FacturaExtractor',
    'BoletaExtractor',
    'PercepcionExtractor'
]