# src/models/__init__.py
"""
📁 MODELOS - PUNTO DE ENTRADA
Exporta todos los modelos para facilitar su uso
"""

from .factura_compra import FacturaCompra
from .boleta_venta import BoletaVenta
from .percepcion import Percepcion

__all__ = [
    'FacturaCompra',
    'BoletaVenta',
    'Percepcion'
]