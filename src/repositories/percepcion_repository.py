# src/repositories/percepcion_repository.py
"""
📁 REPOSITORIO DE PERCEPCIONES
"""

from typing import Optional, List
from datetime import datetime
from .base_repository import BaseRepository
from src.models.percepcion import Percepcion

class PercepcionRepository(BaseRepository[Percepcion]):
    
    def __init__(self):
        super().__init__(Percepcion)
    
    def _convertir_fecha(self, fecha_str):
        if not fecha_str:
            return None
        if isinstance(fecha_str, datetime):
            return fecha_str.date() if hasattr(fecha_str, 'date') else fecha_str
        if isinstance(fecha_str, str):
            try:
                return datetime.strptime(fecha_str, '%d/%m/%Y').date()
            except ValueError:
                try:
                    return datetime.strptime(fecha_str, '%Y-%m-%d').date()
                except ValueError:
                    return None
        return fecha_str
    
    def guardar(self, datos: dict) -> Percepcion:
        mapeo = {
            'numero': 'numero_doc',
            'serie': 'serie',
            'fecha_emision': 'fecha_emision',
            'factura_asociada': 'factura_asociada',
            'proveedor': 'proveedor',
            'ruc': 'ruc_proveedor',
            'monto': 'monto',
            'ruta_pdf': 'ruta_pdf',
            'observaciones': 'observaciones',
            'mes': 'mes',
            'año': 'año',
        }
        
        datos_mapeados = {}
        for clave_extractor, valor in datos.items():
            clave_modelo = mapeo.get(clave_extractor, clave_extractor)
            
            if clave_modelo == 'fecha_emision':
                valor = self._convertir_fecha(valor)
            
            datos_mapeados[clave_modelo] = valor
        
        return super().guardar(datos_mapeados)
    
    def obtener_por_numero(self, numero: str) -> Optional[Percepcion]:
        return self.db.query(Percepcion).filter(Percepcion.numero_doc == numero).first()
    
    def existe_numero(self, numero: str) -> bool:
        return self.obtener_por_numero(numero) is not None
    
    def obtener_por_mes(self, mes: int, año: int) -> List[Percepcion]:
        todas = self.obtener_todos()
        return [p for p in todas if p.mes == mes and p.año == año]
