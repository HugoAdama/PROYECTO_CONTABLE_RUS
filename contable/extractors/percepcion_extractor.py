"""
EXTRACTOR PERCEPCIÓN - VERSIÓN CORREGIDA
"""
from contable.extractors.base_extractor import BaseExtractor
from typing import Dict, Any
from datetime import datetime

class PercepcionExtractor(BaseExtractor):
    """Extractor para percepciones"""

    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """Extrae datos de una percepción desde un PDF"""
        # Leer el PDF y extraer texto
        self.extraer_texto(ruta_pdf)

        if not self.texto:
            return None

        datos = {
            'ruta_pdf': ruta_pdf,
            'tipo': 'percepcion'
        }

        # Número de comprobante
        numero = self.buscar_patron(r'(P[0-9]{3}\s*-\s*[0-9]{5,12})')
        datos['numero_comprobante'] = numero.replace(' ', '') if numero else 'DESCONOCIDO'

        # Proveedor
        proveedor = self.buscar_patron(r'(?:PROVEEDOR|RAZON SOCIAL|EMPRESA)\s*[.:]?\s*([^\n]{5,50})')
        datos['proveedor'] = proveedor or 'PROVEEDOR NO IDENTIFICADO'

        # RUC del proveedor
        ruc = self.buscar_patron(r'RUC\s*[.:]?\s*(\d{11})')
        datos['ruc_proveedor'] = ruc or ''

        # Fecha de emisión
        fecha = self.extraer_fecha(r'FECHA\s*(?:DE EMISION)?\s*[.:]?\s*(\d{2}/\d{2}/\d{4})')
        datos['fecha_emision'] = fecha or datetime.now().strftime('%Y-%m-%d')

        # Monto
        monto = self.buscar_patron(r'(?:IMPORTE\s+TOTAL\s+PERCIBIDO|MONTO|TOTAL|PERCEPCION)\s*[.:]?\s*(?:S\/?\s*)?([\d,]+\.?\d{0,2})')
        if monto:
            monto_val = float(monto.replace(',', ''))
            datos['monto'] = monto_val
            datos['monto_percibido'] = monto_val

        # Porcentaje (si existe)
        porcentaje = self.buscar_patron(r'PORCENTAJE\s*[.:]?\s*([\d,]+\.?\d{0,2})\s*%')
        if porcentaje:
            datos['porcentaje'] = float(porcentaje.replace(',', ''))
        else:
            datos['porcentaje'] = 2.0  # Porcentaje por defecto (RUS)

        return datos
