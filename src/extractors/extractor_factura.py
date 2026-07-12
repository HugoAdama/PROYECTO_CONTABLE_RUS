# src/extractors/extractor_factura.py
"""
📄 EXTRACTOR FACTURA NATURA - VERSIÓN CORREGIDA
"""

from src.extractors.base_extractor import BaseExtractor
from typing import Dict, Any
from datetime import datetime

class ExtractorFacturaNatura(BaseExtractor):
    """Extractor específico para facturas de Natura"""

    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """Extrae datos de una factura de Natura"""
        
        self.extraer_texto(ruta_pdf)
        
        datos = {
            'ruta_pdf': ruta_pdf,
            'tipo': 'factura_compra',
            'proveedor': 'Natura'
        }
        
        # Extraer número de factura
        numero = self.buscar_patron(r'FACTURA\s*(?:N°|Nº|NUMERO)?\s*([\d\-]+)')
        if numero:
            partes = numero.split('-')
            datos['numero_factura'] = partes[-1] if partes else numero
        else:
            fallback = self.buscar_patron(r'(\d{8})')
            datos['numero_factura'] = fallback or 'DESCONOCIDO'
        
        # Extraer RUC del proveedor
        ruc = self.buscar_patron(r'RUC\s*[:.]?\s*(\d{11})')
        datos['ruc_proveedor'] = ruc or '20101796532'
        
        # Extraer nombre del proveedor
        nombre = self.buscar_patron(r'(?:PROVEEDOR|NATURA)\s*[:.]?\s*([^\n]{5,50})')
        datos['proveedor'] = nombre or 'NATURA COSMETICOS S.A.'
        
        # Extraer fecha de emisión
        fecha = self.extraer_fecha(r'FECHA\s*(?:DE EMISION)?\s*[:.]?\s*(\d{2}/\d{2}/\d{4})')
        if fecha:
            datos['fecha_emision'] = fecha
        else:
            datos['fecha_emision'] = datetime.now()
        
        # Extraer montos
        total = self.extraer_monto(r'TOTAL\s*(?:S/|S\.)?\s*([\d,]+\.\d{2})')
        datos['total_pagar'] = total or 0.0
        
        igv = self.extraer_monto(r'IGV\s*(?:S/|S\.)?\s*([\d,]+\.\d{2})')
        datos['igv'] = igv or 0.0
        
        gravado = self.extraer_monto(r'(?:SUB\s*TOTAL|GRAVADO)\s*(?:S/|S\.)?\s*([\d,]+\.\d{2})')
        datos['sub_total'] = gravado or (datos['total_pagar'] - datos['igv'])
        
        # ⭐ MES Y AÑO (USANDO "anio" SIN TILDE)
        if 'fecha_emision' in datos:
            datos['mes'] = datos['fecha_emision'].month
            datos['anio'] = datos['fecha_emision'].year  # ← Cambiado de "año" a "anio"
        else:
            datos['mes'] = datetime.now().month
            datos['anio'] = datetime.now().year  # ← Cambiado de "año" a "anio"
        
        return datos