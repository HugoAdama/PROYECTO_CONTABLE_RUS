# src/extractors/extractor_boleta.py
"""
🧾 EXTRACTOR BOLETA - VERSIÓN CORREGIDA
"""

from src.extractors.base_extractor import BaseExtractor
from typing import Dict, Any
from datetime import datetime

class ExtractorBoleta(BaseExtractor):
    """Extractor para boletas de venta genéricas"""

    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """Extrae datos de una boleta de venta"""
        
        self.extraer_texto(ruta_pdf)
        
        datos = {
            'ruta_pdf': ruta_pdf,
            'tipo': 'boleta_venta'
        }
        
        # Número de boleta
        numero = self.buscar_patron(r'BOLETA\s*(?:N°|Nº|NUMERO)?\s*([\d\-]+)')
        if numero:
            partes = numero.split('-')
            datos['numero_boleta'] = partes[-1] if partes else numero
        else:
            datos['numero_boleta'] = 'DESCONOCIDO'
        
        # RUC del cliente
        ruc = self.buscar_patron(r'RUC\s*[:.]?\s*(\d{11})')
        datos['ruc_cliente'] = ruc or ''
        
        # Nombre del cliente
        nombre = self.buscar_patron(r'(?:CLIENTE|NOMBRE)\s*[:.]?\s*([^\n]{5,50})')
        datos['cliente'] = nombre or 'CLIENTE NO IDENTIFICADO'
        
        # Fecha
        fecha = self.extraer_fecha(r'FECHA\s*(?:DE EMISION)?\s*[:.]?\s*(\d{2}/\d{2}/\d{4})')
        datos['fecha_emision'] = fecha or datetime.now()
        
        # Montos
        total = self.extraer_monto(r'TOTAL\s*(?:S/|S\.)?\s*([\d,]+\.\d{2})')
        datos['total_pagar'] = total or 0.0
        
        igv = self.extraer_monto(r'IGV\s*(?:S/|S\.)?\s*([\d,]+\.\d{2})')
        datos['igv'] = igv or 0.0
        
        datos['sub_total'] = datos['total_pagar'] - datos['igv']
        
        # ⭐ MES Y AÑO (USANDO "anio" SIN TILDE)
        datos['mes'] = datos['fecha_emision'].month
        datos['anio'] = datos['fecha_emision'].year  # ← Cambiado de "año" a "anio"
        
        return datos