# src/repositories/boleta_repository.py
from src.repositories.base_repository import BaseRepository
from src.models.boleta_venta import BoletaVenta
from typing import Optional, List

class BoletaRepository(BaseRepository):
    def __init__(self, session=None):
        super().__init__(BoletaVenta, session)

    def obtener_por_numero(self, numero: str) -> Optional[BoletaVenta]:
        return self.session.query(BoletaVenta).filter_by(numero_boleta=numero).first()

    def obtener_total_mes(self, mes: int, anio: int) -> float:
        resultado = self.session.query(self.model_class.total_pagar).filter_by(mes=mes, anio=anio).all()
        return sum([r[0] for r in resultado]) if resultado else 0.0