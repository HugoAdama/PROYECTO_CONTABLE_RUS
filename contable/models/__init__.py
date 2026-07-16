"""Modelos de persistencia de Contable RUS."""

from contable.models.boleta_venta import BoletaVenta
from contable.models.factura_compra import FacturaCompra
from contable.models.percepcion import Percepcion


__all__ = [
    "FacturaCompra",
    "BoletaVenta",
    "Percepcion",
]
