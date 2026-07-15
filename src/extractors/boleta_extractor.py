"""
EXTRACTOR BOLETA - VERSIÓN PARA RUS (SUNAT)
"""
from src.extractors.base_extractor import BaseExtractor
from typing import Dict, Any
from datetime import datetime
import re

class BoletaExtractor(BaseExtractor):
    """Extractor específico para boletas de venta electrónicas (SUNAT)"""

    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """Extrae datos de una boleta de venta desde un PDF"""
        self.extraer_texto(ruta_pdf)
        
        if not self.texto:
            return None

        datos = {
            'ruta_pdf': ruta_pdf,
            'tipo': 'boleta_venta'
        }

        # ============================================================
        # Número de Boleta (formato: EB01-302)
        # ============================================================
        num_match = re.search(r'BOLETA\s*DE\s*VENTA\s*ELECTRONICA\s*RUC:\s*\d+\s*([A-Z0-9]+-[0-9]+)', self.texto, re.IGNORECASE)
        if num_match:
            datos['numero_boleta'] = num_match.group(1).strip()
        else:
            # Fallback: buscar patrón EB01-XXX
            fallback = re.search(r'(EB[0-9]+-[0-9]+)', self.texto, re.IGNORECASE)
            datos['numero_boleta'] = fallback.group(1) if fallback else 'DESCONOCIDO'

        # ============================================================
        # RUC del Cliente (formato: RUC: 15117337437)
        # ============================================================
        ruc_match = re.search(r'RUC\s*[:]?\s*(\d{11})', self.texto, re.IGNORECASE)
        if ruc_match:
            datos['ruc_cliente'] = ruc_match.group(1).strip()
        else:
            datos['ruc_cliente'] = ''

        # ============================================================
        # Nombre del Cliente (formato: Señor(es) : INACIA CHU)
        # ============================================================
        cliente_match = re.search(r'Señor(?:es)?\s*[:]?\s*([^\n]{3,50})', self.texto, re.IGNORECASE)
        if cliente_match:
            nombre = cliente_match.group(1).strip()
            # Limpiar si hay texto extra
            nombre = re.sub(r'\s+Tipo\s+de\s+Moneda.*$', '', nombre)
            datos['cliente'] = nombre
        else:
            datos['cliente'] = 'CLIENTE NO IDENTIFICADO'

        # ============================================================
        # Fecha de Emisión (formato: Fecha de Emisión : 31/05/2026)
        # ============================================================
        fecha_match = re.search(r'Fecha\s*de\s*Emisión\s*[:]?\s*(\d{2}/\d{2}/\d{4})', self.texto, re.IGNORECASE)
        if fecha_match:
            fecha_str = fecha_match.group(1)
            # Convertir a formato YYYY-MM-DD
            try:
                fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
                datos['fecha_emision'] = fecha_obj.strftime('%Y-%m-%d')
            except ValueError:
                datos['fecha_emision'] = fecha_str.replace('/', '-')
        else:
            # Fallback: buscar cualquier fecha
            fecha_fallback = re.search(r'(\d{2}/\d{2}/\d{4})', self.texto)
            if fecha_fallback:
                fecha_str = fecha_fallback.group(1)
                try:
                    fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
                    datos['fecha_emision'] = fecha_obj.strftime('%Y-%m-%d')
                except ValueError:
                    datos['fecha_emision'] = fecha_str.replace('/', '-')
            else:
                datos['fecha_emision'] = datetime.now().strftime('%Y-%m-%d')

        # ============================================================
        # Montos: Buscar Importe Total
        # ============================================================
        total_match = re.search(r'Importe\s*Total\s*[:]?\s*S\/\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
        if total_match:
            total_str = total_match.group(1).replace(',', '')
            datos['total_pagar'] = float(total_str)

        # Buscar IGV (puede ser 0.00)
        igv_match = re.search(r'IGV\s*[:]?\s*S\/\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
        if igv_match:
            igv_str = igv_match.group(1).replace(',', '')
            datos['igv'] = float(igv_str)
        else:
            # Si no hay IGV, calcularlo como 18% del total (si total > 0)
            if datos.get('total_pagar', 0) > 0:
                # total = sub_total * 1.18, entonces sub_total = total / 1.18
                total = datos['total_pagar']
                datos['sub_total'] = round(total / 1.18, 2)
                datos['igv'] = round(total - datos['sub_total'], 2)
            else:
                datos['sub_total'] = 0.0
                datos['igv'] = 0.0

        # Buscar Sub Total (si existe)
        sub_total_match = re.search(r'Sub\s*Total\s*[:]?\s*S\/\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
        if sub_total_match:
            sub_str = sub_total_match.group(1).replace(',', '')
            datos['sub_total'] = float(sub_str)

        # ============================================================
        # Asegurar valores por defecto
        # ============================================================
        datos.setdefault('sub_total', 0.0)
        datos.setdefault('igv', 0.0)
        datos.setdefault('total_pagar', 0.0)
        datos.setdefault('ruc_cliente', '')

        return datos