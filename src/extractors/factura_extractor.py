"""
EXTRACTOR FACTURA - VERSIÓN PARA NATURA
"""
from src.extractors.base_extractor import BaseExtractor
from typing import Dict, Any
from datetime import datetime
import re

class FacturaExtractor(BaseExtractor):
    """Extractor específico para facturas de Natura Cosméticos S.A."""

    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """Extrae datos de una factura de Natura desde un PDF"""
        self.extraer_texto(ruta_pdf)
        
        if not self.texto:
            return None

        datos = {
            'ruta_pdf': ruta_pdf,
            'tipo': 'factura_compra',
            'proveedor': 'NATURA COSMETICOS S.A.'
        }

        # ============================================================
        # RUC del proveedor (formato: R.U.C: 20101796532)
        # ============================================================
        ruc_match = re.search(r'R\.U\.C\s*[:]?\s*(\d{11})', self.texto, re.IGNORECASE)
        if ruc_match:
            datos['ruc_proveedor'] = ruc_match.group(1).strip()
        else:
            datos['ruc_proveedor'] = '20101796532'

        # ============================================================
        # Número de Factura (formato: F033 - 00334797)
        # ============================================================
        num_match = re.search(r'FACTURA\s*DE\s*VENTA\s*ELECTRÓNICA\s*N°\s*([A-Z0-9]+\s*[-]\s*[0-9]+)', self.texto, re.IGNORECASE)
        if num_match:
            numero_raw = num_match.group(1).strip()
            # Limpiar: eliminar espacios para obtener F033-00334797
            numero_limpio = re.sub(r'\s+', '', numero_raw)
            datos['numero_factura'] = numero_limpio
        else:
            # Fallback
            fallback = re.search(r'(F[0-9]{3}\s*[-]\s*[0-9]+)', self.texto, re.IGNORECASE)
            if fallback:
                datos['numero_factura'] = re.sub(r'\s+', '', fallback.group(1))
            else:
                datos['numero_factura'] = 'DESCONOCIDO'

        # ============================================================
        # Fecha de Emisión (formato: Fecha Emisión: 08/05/2026)
        # ============================================================
        fecha_match = re.search(r'Fecha\s*Emisión\s*[:]?\s*(\d{2}/\d{2}/\d{4})', self.texto, re.IGNORECASE)
        if fecha_match:
            fecha_str = fecha_match.group(1)
            try:
                fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
                datos['fecha_emision'] = fecha_obj.strftime('%Y-%m-%d')
            except ValueError:
                datos['fecha_emision'] = fecha_str.replace('/', '-')
        else:
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
        # Montos: Buscar en la tabla de totales
        # ============================================================
        # Buscar Sub Total
        sub_total_match = re.search(r'Sub Total\s*S\/?\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
        if sub_total_match:
            datos['sub_total'] = float(sub_total_match.group(1).replace(',', ''))

        # Buscar IGV 18%
        igv_match = re.search(r'IGV\s*18%\s*S\/?\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
        if igv_match:
            datos['igv'] = float(igv_match.group(1).replace(',', ''))

        # Buscar Total con Descuento
        total_match = re.search(r'Total\s*con\s*Dscto\.\s*S\/?\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
        if total_match:
            datos['total_pagar'] = float(total_match.group(1).replace(',', ''))

        # Buscar Percepción
        percepcion_match = re.search(r'Percepción\s*2%\s*S\/?\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
        if percepcion_match:
            datos['percepcion'] = float(percepcion_match.group(1).replace(',', ''))

        # Si no se encontró total con descuento, buscar Total a Pagar
        if 'total_pagar' not in datos:
            total_final_match = re.search(r'Total\s*a\s*Pagar\s*S\/?\s*([\d,]+\.?\d{0,2})', self.texto, re.IGNORECASE)
            if total_final_match:
                datos['total_pagar'] = float(total_final_match.group(1).replace(',', ''))

        # ============================================================
        # Asegurar valores por defecto
        # ============================================================
        datos.setdefault('sub_total', 0.0)
        datos.setdefault('igv', 0.0)
        datos.setdefault('total_pagar', 0.0)
        datos.setdefault('percepcion', 0.0)

        return datos