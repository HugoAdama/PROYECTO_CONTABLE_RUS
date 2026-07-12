# src/extractors/extractor_boleta.py
"""
📄 EXTRACTOR DE BOLETAS - VERSIÓN CORREGIDA
"""

from .base_extractor import ExtractorBase
import re
import json
from pathlib import Path

class ExtractorBoleta(ExtractorBase):
    """
    Extractor específico para boletas de venta.
    """
    
    def __init__(self):
        super().__init__()
        
        # Patrones basados en el formato real
        self.patrones = {
            'numero': r'BOLETA\s*DE\s*VENTA\s*ELECTRONICA.*?(EB\d{2}-\d{3})',
            'serie': r'(EB\d{2})',
            'fecha_emision': r'Fecha\s*de\s*Emisión\s*:\s*(\d{2}/\d{2}/\d{4})',
            'ruc_emisor': r'RUC:\s*(\d{11})',
            'nombre_cliente': r'Señor\(es\)\s*:\s*(.*?)(?:\n|$)',
            'direccion_cliente': r'JR\.\s*(.*?)(?:\n|$)',
            'monto_total': r'Importe\s*Total\s*:\s*S/\s*([\d,]+\.\d{2})',
        }
        
        # Patrón para productos
        self.patron_producto = r'(\d+\.?\d*)\s+UNIDAD\s+(.*?)\s+([\d,]+\.\d{2})\s+0\.00\s+([\d,]+\.\d{2})'
    
    def extraer(self, ruta_pdf: str) -> dict:
        """
        Extrae todos los datos de la boleta.
        """
        texto = self._leer_pdf(ruta_pdf)
        if not texto:
            return None
        
        datos = {}
        
        # 1. Extraer con patrones principales
        for campo, patron in self.patrones.items():
            valor = self._buscar_patron(patron)
            if valor:
                if campo == 'monto_total':
                    datos[campo] = self._limpiar_monto(valor)
                elif campo == 'fecha_emision':
                    fecha = self._extraer_fecha(patron)
                    if fecha:
                        datos[campo] = fecha
                else:
                    datos[campo] = valor.strip()
        
        # 2. Si no se encontró el número, extraer del nombre del archivo
        if 'numero' not in datos or datos['numero'] == '':
            nombre = Path(ruta_pdf).stem
            # Buscar EB01-302 en el nombre
            match = re.search(r'EB\d{2}-\d{3}', nombre)
            if match:
                datos['numero'] = match.group(0)
            else:
                datos['numero'] = nombre[:15]
        
        # 3. Extraer serie
        if 'serie' not in datos and 'numero' in datos:
            match = re.search(r'(EB\d{2})', datos['numero'])
            if match:
                datos['serie'] = match.group(1)
        
        # 4. Si no hay cliente, poner "Cliente General"
        if 'nombre_cliente' not in datos or datos['nombre_cliente'] == '':
            datos['nombre_cliente'] = 'Cliente General'
        
        # 5. Extraer productos
        productos = self._extraer_productos(self.patron_producto)
        if productos:
            datos['productos'] = json.dumps(productos, ensure_ascii=False)
            datos['cantidad_productos'] = len(productos)
        else:
            datos['productos'] = json.dumps([])
            datos['cantidad_productos'] = 0
        
        # 6. Nombre del emisor
        datos['nombre_emisor'] = 'DE LA CRUZ MELCHOR MARIA TERESA'
        
        # 7. Tipo de comprobante
        datos['tipo_comprobante'] = 'BOLETA'
        
        # 8. Estado
        datos['estado'] = 'procesado'
        
        # 9. Observaciones
        observaciones = []
        if not datos.get('numero'):
            observaciones.append("Número de boleta no encontrado")
        if not datos.get('fecha_emision'):
            observaciones.append("Fecha de emisión no encontrada")
        if datos.get('monto_total', 0) == 0:
            observaciones.append("Monto total es 0 - verificar")
        
        datos['observaciones'] = ' | '.join(observaciones) if observaciones else 'OK'
        
        # 10. Agregar ruta del PDF
        datos['ruta_pdf'] = ruta_pdf
        
        return datos
    
    def _extraer_productos(self, patron):
        """
        Extrae productos del texto.
        """
        productos = []
        matches = re.findall(patron, self.texto, re.IGNORECASE)
        
        for match in matches:
            if len(match) >= 4:
                productos.append({
                    'cantidad': self._limpiar_monto(match[0]),
                    'descripcion': match[1].strip(),
                    'precio_unitario': self._limpiar_monto(match[2]),
                    'total': self._limpiar_monto(match[3])
                })
        
        return productos