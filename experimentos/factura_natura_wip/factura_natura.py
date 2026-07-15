# src/extractors/factura_natura.py
# ================================

import re
from typing import Dict, Any
from datetime import datetime
from .base import BaseExtractor

class FacturaNaturaExtractor(BaseExtractor):
    """Extractor para facturas de Natura Cosméticos."""
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extrae datos de una factura Natura."""
        data = {
            'numero': '',
            'ruc_emisor': '',
            'ruc_cliente': '',
            'nombre_cliente': '',
            'fecha_emision': datetime.now().strftime('%d/%m/%Y'),
            'monto_total': 0.0,
            'monto_base': 0.0,
            'percepcion': 0.0,
            'ciclo': ''
        }
        
        # Buscar "N° F033 - 00330623"
        num_match = re.search(r'N°\s*F033\s*[-–]\s*(\d+)', text)
        if num_match:
            data['numero'] = f"F033-{num_match.group(1)}"
        
        # Buscar "R.U.C: 20101796532"
        ruc_match = re.search(r'R\.U\.C[:\s]*(\d{11})', text)
        if ruc_match:
            data['ruc_emisor'] = ruc_match.group(1)
        
        # Buscar "DNI/RUC: 15117337437"
        ruc_cli = re.search(r'DNI/RUC[:\s]*(\d{11})', text)
        if ruc_cli:
            data['ruc_cliente'] = ruc_cli.group(1)
        
        # Buscar "Nombre CB: DE LA CRUZ MELCHOR MARIA TERESA"
        nom_match = re.search(r'Nombre CB[:\s]*([^\n\r]+)', text)
        if nom_match:
            data['nombre_cliente'] = nom_match.group(1).strip()
        
        # Buscar "Fecha Emisión: 12/05/2026"
        fecha_match = re.search(r'Fecha Emisión[:\s]*(\d{1,2}/\d{1,2}/\d{4})', text)
        if fecha_match:
            data['fecha_emision'] = fecha_match.group(1)
        
        # Buscar "Ciclo: 202608"
        ciclo_match = re.search(r'Ciclo[:\s]*(\d{6})', text)
        if ciclo_match:
            data['ciclo'] = ciclo_match.group(1)
        
        # Buscar "Total a Pagar S/ 191.70" o "(A) Total con Dscto. S/ 187.94"
        total_match = re.search(r'Total a Pagar[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if total_match:
            data['monto_total'] = self._parse_monto(total_match.group(1))
        else:
            total_match2 = re.search(r'\(A\)\s*Total con Dscto[.:\s]*S/?\s*([\d,]+\.?\d*)', text)
            if total_match2:
                data['monto_total'] = self._parse_monto(total_match2.group(1))
        
        # Buscar "(B) Percepcion 2% S/ 3.76"
        perc_match = re.search(r'\(B\)\s*Percepción[.\s]*S/?\s*([\d,]+\.?\d*)', text)
        if perc_match:
            data['percepcion'] = self._parse_monto(perc_match.group(1))
        
        # Buscar "Sub Total S/ 159.27"
        base_match = re.search(r'Sub Total[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if base_match:
            data['monto_base'] = self._parse_monto(base_match.group(1))
        
        return data
