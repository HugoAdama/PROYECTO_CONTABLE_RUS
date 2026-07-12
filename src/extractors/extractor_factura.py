# src/extractors/extractor_factura.py
"""
📄 EXTRACTOR DE FACTURAS NATURA - VERSIÓN CORREGIDA
"""

from .base_extractor import ExtractorBase
import re
import json
from pathlib import Path

class ExtractorFacturaNatura(ExtractorBase):
    """Extractor específico para facturas de Natura."""
    
    def __init__(self):
        super().__init__()
        
        self.patrones = {
            'ruc': r'R\.U\.C\s*[:.]?\s*(\d{11})',
            'numero': r'FACTURA\s*DE\s*VENTA\s*ELECTRÓNICA\s*N°\s*(F\d{3}\s*[-–]\s*\d{8})',
            'serie': r'(F\d{3})',
            'fecha_emision': r'(?:Ficha\s*de\s*Pago|Fecha\s*Emisión)\s*[:.]?\s*(\d{2}/\d{2}/\d{4})',
            'fecha_vencimiento': r'Fecha\s*Vencimiento\s*[:.]?\s*(\d{2}/\d{2}/\d{4})',
            'sub_total': r'Sub\s*Total\s*S/\s*([\d,]+\.\d{2})',
            'igv': r'IGV\s*18%\s*S/\s*([\d,]+\.\d{2})',
            'total_con_descuento': r'\(A\)\s*Total\s*con\s*Dsc\.to\.\s*S/\s*([\d,]+\.\d{2})',
            'percepcion': r'\(B\)\s*Percepcion\s*(?:2%)?\s*S/\s*([\d,]+\.\d{2})',
            'total_pagar': r'Importe\s*TOTAL\s*a\s*pagar\s*[:.]?\s*S/\s*([\d,]+\.\d{2})',
            'proveedor': r'(Natura Cosméticos S\.A\.)',
        }
        
        self.patron_producto = r'(\d+)\s+([^\n]+?)\s+([\d,]+\.\d{2})'
    
    def extraer(self, ruta_pdf: str) -> dict:
        """Extrae todos los datos de la factura."""
        texto = self._leer_pdf(ruta_pdf)
        if not texto:
            return None
        
        datos = {}
        
        # 1. Extraer con patrones
        for campo, patron in self.patrones.items():
            valor = self._buscar_patron(patron)
            if valor:
                if campo in ['sub_total', 'igv', 'total_con_descuento', 'percepcion', 'total_pagar']:
                    datos[campo] = self._limpiar_monto(valor)
                elif campo in ['fecha_emision', 'fecha_vencimiento']:
                    fecha = self._extraer_fecha(patron)
                    if fecha:
                        datos[campo] = fecha
                else:
                    datos[campo] = valor.strip()
        
        # 2. Buscar total manualmente (si no se encontró)
        if 'total_pagar' not in datos or datos.get('total_pagar', 0) == 0:
            patrones_total = [
                r'Importe\s*TOTAL\s*a\s*pagar\s*[:.]?\s*S/\s*([\d,]+\.\d{2})',
                r'Total\s*a\s*Pagar\s*[:.]?\s*S/\s*([\d,]+\.\d{2})',
                r'TOTAL\s*A\s*PAGAR\s*[:.]?\s*S/\s*([\d,]+\.\d{2})',
                r'Total\s*[:.]?\s*S/\s*([\d,]+\.\d{2})',
                r'IMPORTE\s*TOTAL\s*[:.]?\s*S/\s*([\d,]+\.\d{2})',
            ]
            
            for patron in patrones_total:
                match = re.search(patron, self.texto, re.IGNORECASE)
                if match:
                    total = self._limpiar_monto(match.group(1))
                    # Solo aceptar si es mayor a 100 (descartar percepciones de 9.23)
                    if total > 100:
                        datos['total_pagar'] = total
                        break
        
        # 3. Buscar percepción manualmente
        if 'percepcion' not in datos:
            match = re.search(r'Percepcion\s*(?:2%)?\s*S/\s*([\d,]+\.\d{2})', self.texto, re.IGNORECASE)
            if match:
                datos['percepcion'] = self._limpiar_monto(match.group(1))
        
        # 4. RUC por defecto
        if 'ruc' not in datos:
            datos['ruc'] = '20101796532'
        
        # 5. Productos
        productos = self._extraer_productos()
        if productos:
            datos['productos'] = json.dumps(productos, ensure_ascii=False)
            datos['cantidad_productos'] = len(productos)
        else:
            datos['productos'] = json.dumps([])
            datos['cantidad_productos'] = 0
        
        # 6. Número de factura desde nombre de archivo
        if 'numero' not in datos:
            nombre = Path(ruta_pdf).stem
            match = re.search(r'F\d{3}[-–]\d{8}', nombre)
            if match:
                datos['numero'] = match.group(0)
            else:
                datos['numero'] = nombre[:15]
        
        # 7. Serie
        if 'serie' not in datos and 'numero' in datos:
            match = re.search(r'(F\d{3})', datos['numero'])
            if match:
                datos['serie'] = match.group(1)
        
        # 8. Proveedor por defecto
        if 'proveedor' not in datos:
            datos['proveedor'] = 'NATURA COSMETICOS S.A.'
        
        # 9. Tipo y estado
        datos['tipo_comprobante'] = 'FACTURA'
        datos['estado'] = 'procesado'
        
        # 10. Observaciones
        observaciones = []
        if not datos.get('numero'):
            observaciones.append("Número de factura no encontrado")
        if not datos.get('fecha_emision'):
            observaciones.append("Fecha de emisión no encontrada")
        if datos.get('total_pagar', 0) == 0:
            observaciones.append("Total a pagar es 0 - verificar")
        
        datos['observaciones'] = ' | '.join(observaciones) if observaciones else 'OK'
        
        # 11. Ruta del PDF
        datos['ruta_pdf'] = ruta_pdf
        
        return datos
    
    def _extraer_productos(self):
        """Extrae productos del texto de factura Natura."""
        productos = []
        
        patron_tabla = r'Código producto\s+Cantidad\s+Descripción\s+Total con\s+([\s\S]*?)(?:CONSIDERACIONES|IMPORTE TOTAL|Sub Total|\(A\))'
        match = re.search(patron_tabla, self.texto, re.IGNORECASE)
        
        if match:
            tabla = match.group(1)
            lineas = tabla.strip().split('\n')
            
            i = 0
            while i < len(lineas):
                if i + 1 < len(lineas):
                    codigo_linea = lineas[i].strip()
                    desc_linea = lineas[i+1].strip()
                    
                    codigo_match = re.search(r'(\d+)\s+(\d+)', codigo_linea)
                    
                    if codigo_match:
                        codigo = codigo_match.group(1)
                        cantidad = int(codigo_match.group(2))
                        
                        desc_match = re.search(r'(.+?)\s+([\d,]+\.\d{2})$', desc_linea)
                        if desc_match:
                            descripcion = desc_match.group(1).strip()
                            total = self._limpiar_monto(desc_match.group(2))
                            
                            productos.append({
                                'codigo': codigo,
                                'cantidad': cantidad,
                                'descripcion': descripcion,
                                'total': total
                            })
                i += 2
        
        return productos