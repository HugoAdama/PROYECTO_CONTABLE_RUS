"""Repositorios de acceso a datos de Contable RUS."""

from contable.repositories.base_repository import BaseRepository
from contable.repositories.boleta_repository import BoletaRepository
from contable.repositories.factura_repository import FacturaRepository
from contable.repositories.percepcion_repository import PercepcionRepository


__all__ = [
    "BaseRepository",
    "FacturaRepository",
    "BoletaRepository",
    "PercepcionRepository",
]
