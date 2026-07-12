# src/repositories/factura_repository.py
from src.repositories.base_repository import BaseRepository
from src.models.factura_compra import FacturaCompra
from typing import Optional, List

class FacturaRepository(BaseRepository):
    def __init__(self, session=None):
        super().__init__(FacturaCompra, session)

    def obtener_por_numero(self, numero: str) -> Optional[FacturaCompra]:
        return self.session.query(FacturaCompra).filter_by(numero_factura=numero).first()

    def obtener_total_mes(self, mes: int, anio: int) -> float:
        resultado = self.session.query(self.model_class.total_pagar).filter_by(mes=mes, anio=anio).all()
        return sum([r[0] for r in resultado]) if resultado else 0.0