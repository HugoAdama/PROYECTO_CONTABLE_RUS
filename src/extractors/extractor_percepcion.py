# src/extractors/extractor_percepcion.py
"""
💰 EXTRACTOR PERCEPCIÓN - VERSIÓN CORREGIDA
"""

from src.extractors.base_extractor import BaseExtractor
from typing import Dict, Any
from datetime import datetime

class ExtractorPercepcion(BaseExtractor):
    """Extractor para percepciones"""

    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """Extrae datos de una percepción"""
        
        self.extraer_texto(ruta_pdf)
        
        datos = {
            'ruta_pdf': ruta_pdf,
            'tipo': 'percepcion'
        }
        
        # Número de comprobante
        numero = self.buscar_patron(r'(?:PERCEPCION|N°|Nº)\s*([\d\-]+)')
        datos['numero_comprobante'] = numero or 'DESCONOCIDO'
        
        # Proveedor
        proveedor = self.buscar_patron(r'(?:PROVEEDOR|EMPRESA)\s*[:.]?\s*([^\n]{5,50})')
        datos['proveedor'] = proveedor or 'PROVEEDOR NO IDENTIFICADO'
        
        # RUC
        ruc = self.buscar_patron(r'RUC\s*[:.]?\s*(\d{11})')
        datos['ruc_proveedor'] = ruc or ''
        
        # Fecha
        fecha = self.extraer_fecha(r'FECHA\s*(?:DE EMISION)?\s*[:.]?\s*(\d{2}/\d{2}/\d{4})')
        datos['fecha_emision'] = fecha or datetime.now()
        
        # Monto
        monto = self.extraer_monto(r'(?:MONTO|S/)\s*(?:S/|S\.)?\s*([\d,]+\.\d{2})')
        datos['monto'] = monto or 0.0
        
        # Porcentaje
        porcentaje = self.buscar_patron(r'(\d+\.?\d*)\s*%')
        datos['porcentaje'] = float(porcentaje) if porcentaje else 2.0
        
        datos['monto_percibido'] = datos['monto'] * (datos['porcentaje'] / 100)
        
        # ⭐ MES Y AÑO (USANDO "anio" SIN TILDE)
        datos['mes'] = datos['fecha_emision'].month
        datos['anio'] = datos['fecha_emision'].year  # ← Cambiado de "año" a "anio"
        
        return datos