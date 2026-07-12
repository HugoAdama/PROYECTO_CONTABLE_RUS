# src/repositories/percepcion_repository.py
from src.repositories.base_repository import BaseRepository
from src.models.percepcion import Percepcion
from typing import Optional, List

class PercepcionRepository(BaseRepository):
    def __init__(self, session=None):
        super().__init__(Percepcion, session)

    def obtener_por_comprobante(self, numero: str) -> List[Percepcion]:
        return self.session.query(Percepcion).filter_by(numero_comprobante=numero).all()

    def obtener_total_mes(self, mes: int, anio: int) -> float:
        resultado = self.session.query(self.model_class.monto).filter_by(mes=mes, anio=anio).all()
        return sum([r[0] for r in resultado]) if resultado else 0.0