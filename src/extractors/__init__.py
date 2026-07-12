# src/extractors/__init__.py
"""
📁 EXTRACTORES - PUNTO DE ENTRADA
Exporta todos los extractores para facilitar su uso
"""

from .base_extractor import ExtractorBase
from .extractor_factura import ExtractorFacturaNatura
from .extractor_boleta import ExtractorBoleta
from .extractor_percepcion import ExtractorPercepcion
from .proveedores import ProveedorDetector

__all__ = [
    'ExtractorBase',
    'ExtractorFacturaNatura',
    'ExtractorBoleta',
    'ExtractorPercepcion',
    'ProveedorDetector'
]