# src/repositories/factura_repository.py
"""
📁 REPOSITORIO DE FACTURAS - VERSIÓN MEJORADA
Operaciones específicas para facturas de compra
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import and_

from .base_repository import BaseRepository
from src.models.factura_compra import FacturaCompra

class FacturaRepository(BaseRepository[FacturaCompra]):
    """
    Repositorio para operaciones con facturas de compra.
    """
    
    def __init__(self):
        super().__init__(FacturaCompra)
    
    def _convertir_fecha(self, fecha_str):
        """Convierte string de fecha a objeto date."""
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
                    print(f"⚠️ No se pudo convertir fecha: {fecha_str}")
                    return None
        return fecha_str
    
    def guardar(self, datos: dict) -> FacturaCompra:
        """
        Guarda una factura con todos los campos nuevos.
        """
        mapeo = {
            # Datos del proveedor
            'numero': 'numero_factura',
            'ruc': 'ruc_proveedor',
            'proveedor': 'proveedor',
            'direccion': 'direccion_proveedor',
            'telefono': 'telefono_proveedor',
            
            # Datos de la factura
            'fecha_emision': 'fecha_emision',
            'fecha_vencimiento': 'fecha_vencimiento',
            'tipo_comprobante': 'tipo_comprobante',
            'serie': 'serie',
            
            # Desglose de montos
            'sub_total': 'sub_total',
            'igv': 'igv',
            'total_con_descuento': 'total_con_descuento',
            'percepcion': 'percepcion',
            'total_pagar': 'total_pagar',
            'otros_cargos': 'otros_cargos',
            'descuento': 'descuento',
            
            # Productos
            'productos': 'productos',
            'cantidad_productos': 'cantidad_productos',
            
            # Metadatos
            'ruta_pdf': 'ruta_pdf',
            'estado': 'estado',
            'observaciones': 'observaciones',
        }
        
        datos_mapeados = {}
        for clave_extractor, valor in datos.items():
            clave_modelo = mapeo.get(clave_extractor, clave_extractor)
            
            if clave_modelo in ['fecha_emision', 'fecha_vencimiento']:
                valor = self._convertir_fecha(valor)
            
            datos_mapeados[clave_modelo] = valor
        
        return super().guardar(datos_mapeados)
    
    def obtener_por_numero(self, numero: str) -> Optional[FacturaCompra]:
        """Obtiene una factura por su número."""
        return self.db.query(FacturaCompra).filter(
            FacturaCompra.numero_factura == numero
        ).first()
    
    def obtener_por_mes(self, mes: int, año: int) -> List[FacturaCompra]:
        """Obtiene facturas de un mes específico."""
        todas = self.obtener_todos()
        return [f for f in todas if f.fecha_emision and 
                f.fecha_emision.month == mes and 
                f.fecha_emision.year == año]
    
    def obtener_total_compras_mes(self, mes: int, año: int) -> float:
        """Calcula el total de compras de un mes."""
        facturas = self.obtener_por_mes(mes, año)
        return sum(f.total_pagar or 0 for f in facturas)
    
    def obtener_percepciones_mes(self, mes: int, año: int) -> float:
        """Calcula el total de percepciones de un mes."""
        facturas = self.obtener_por_mes(mes, año)
        return sum(f.percepcion or 0 for f in facturas)
    
    def existe_numero(self, numero: str) -> bool:
        """Verifica si ya existe una factura con ese número."""
        return self.obtener_por_numero(numero) is not None