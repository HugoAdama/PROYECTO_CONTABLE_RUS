# src/repositories/boleta_repository.py
"""
📁 REPOSITORIO DE BOLETAS
"""

from typing import Optional, List
from datetime import datetime
from .base_repository import BaseRepository
from src.models.boleta_venta import BoletaVenta

class BoletaRepository(BaseRepository[BoletaVenta]):
    
    def __init__(self):
        super().__init__(BoletaVenta)
    
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
    
    def guardar(self, datos: dict) -> BoletaVenta:
        mapeo = {
            'numero': 'numero_boleta',
            'serie': 'serie',
            'tipo_comprobante': 'tipo_comprobante',
            'fecha_emision': 'fecha_emision',
            'ruc_emisor': 'ruc_emisor',
            'nombre_emisor': 'nombre_emisor',
            'direccion_emisor': 'direccion_emisor',
            'nombre_cliente': 'nombre_cliente',
            'ruc_cliente': 'ruc_cliente',
            'direccion_cliente': 'direccion_cliente',
            'telefono_cliente': 'telefono_cliente',
            'monto_total': 'monto_total',
            'sub_total': 'sub_total',
            'igv': 'igv',
            'descuento': 'descuento',
            'productos': 'productos',
            'cantidad_productos': 'cantidad_productos',
            'descripcion': 'descripcion',
            'ruta_pdf': 'ruta_pdf',
            'estado': 'estado',
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
    
    def obtener_por_numero(self, numero: str) -> Optional[BoletaVenta]:
        return self.db.query(BoletaVenta).filter(BoletaVenta.numero_boleta == numero).first()
    
    def obtener_por_mes(self, mes: int, año: int) -> List[BoletaVenta]:
        todas = self.obtener_todos()
        return [b for b in todas if b.fecha_emision and 
                b.fecha_emision.month == mes and 
                b.fecha_emision.year == año]
    
    def obtener_total_ventas_mes(self, mes: int, año: int) -> float:
        boletas = self.obtener_por_mes(mes, año)
        return sum(b.monto_total or 0 for b in boletas)
    
    def existe_numero(self, numero: str) -> bool:
        return self.obtener_por_numero(numero) is not None
