# src/models/__init__.py
"""
Modelos de la base de datos
"""

from .factura_compra import FacturaCompra
from .boleta_venta import BoletaVenta
from .percepcion import Percepcion

__all__ = [
    'FacturaCompra',
    'BoletaVenta',
    'Percepcion'
]