# src/extractors/percepcion.py
# ============================

import re
from typing import Dict, Any
from datetime import datetime
from .base import BaseExtractor

class PercepcionExtractor(BaseExtractor):
    """Extractor para comprobantes de percepción."""
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extrae datos de una percepción."""
        data = {
            'numero': '',
            'ruc_emisor': '',
            'ruc_cliente': '',
            'nombre_cliente': '',
            'fecha_emision': datetime.now().strftime('%d/%m/%Y'),
            'monto_total': 0.0,
            'monto_base': 0.0,
            'documento_asociado': ''
        }
        
        # Buscar "P003 - 00602821"
        num_match = re.search(r'P003\s*[-–]\s*(\d+)', text)
        if num_match:
            data['numero'] = f"P003-{num_match.group(1)}"
        
        # Buscar "R.U.C: 20101796532"
        ruc_match = re.search(r'R\.U\.C[:\s]*(\d{11})', text)
        if ruc_match:
            data['ruc_emisor'] = ruc_match.group(1)
        
        # Buscar "RUC: 15117337437"
        ruc_cli = re.search(r'RUC[:\s]*(\d{11})', text)
        if ruc_cli:
            data['ruc_cliente'] = ruc_cli.group(1)
        
        # Buscar "Señor(es): DE LA CRUZ MELCHOR MARIA TERESA"
        nom_match = re.search(r'Señor\(es\)[:\s]*([^\n\r]+)', text)
        if nom_match:
            data['nombre_cliente'] = nom_match.group(1).strip()
        
        # Buscar "Fecha de Emisión: 28/05/2026"
        fecha_match = re.search(r'Fecha de Emisión[:\s]*(\d{1,2}/\d{1,2}/\d{4})', text)
        if fecha_match:
            data['fecha_emision'] = fecha_match.group(1)
        
        # Buscar "Factura Electrónica F033-00331167"
        factura_match = re.search(r'Factura\s+Electrónica\s+([A-Z0-9\-]+)', text)
        if factura_match:
            data['documento_asociado'] = factura_match.group(1)
        
        # Buscar "Importe Total Percibido: 8.83"
        perc_match = re.search(r'Importe Total Percibido[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if perc_match:
            data['monto_total'] = self._parse_monto(perc_match.group(1))
        
        # Buscar "BASE: 441.54"
        base_match = re.search(r'BASE[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if base_match:
            data['monto_base'] = self._parse_monto(base_match.group(1))
        
        return data
