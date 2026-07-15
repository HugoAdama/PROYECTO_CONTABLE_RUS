# src/extractors/boleta.py
# ========================

import re
from typing import Dict, Any
from datetime import datetime
from .base import BaseExtractor

class BoletaExtractor(BaseExtractor):
    """Extractor para boletas SUNAT."""
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extrae datos de una boleta."""
        data = {
            'numero': '',
            'ruc_emisor': '',
            'nombre_cliente': '',
            'fecha_emision': datetime.now().strftime('%d/%m/%Y'),
            'monto_total': 0.0
        }
        
        # Buscar "BOLETA DE VENTA ELECTRONICA EB01-302"
        num_match = re.search(r'EB01\s*[-–]\s*(\d+)', text)
        if num_match:
            data['numero'] = f"EB01-{num_match.group(1)}"
        
        # Buscar "RUC: 15117337437"
        ruc_match = re.search(r'RUC[:\s]*(\d{11})', text)
        if ruc_match:
            data['ruc_emisor'] = ruc_match.group(1)
        
        # Buscar "Señor(es): KAROLAY CHAVEZ"
        nom_match = re.search(r'Señor\(es\)[:\s]*([^\n\r]+)', text)
        if nom_match:
            data['nombre_cliente'] = nom_match.group(1).strip()
        
        # Buscar "Fecha de Emisión: 31/05/2026"
        fecha_match = re.search(r'Fecha de Emisión[:\s]*(\d{1,2}/\d{1,2}/\d{4})', text)
        if fecha_match:
            data['fecha_emision'] = fecha_match.group(1)
        
        # Buscar "Importe Total: S/ 200.00"
        total_match = re.search(r'Importe Total[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if total_match:
            data['monto_total'] = self._parse_monto(total_match.group(1))
        
        return data
