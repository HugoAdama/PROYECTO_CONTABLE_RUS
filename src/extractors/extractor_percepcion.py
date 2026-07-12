# src/extractors/extractor_percepcion.py
"""
📄 EXTRACTOR DE PERCEPCIONES
Extrae datos de comprobantes de percepción
"""

from .base_extractor import ExtractorBase
import re
from pathlib import Path

class ExtractorPercepcion(ExtractorBase):
    """
    Extractor para comprobantes de percepción de Natura.
    """
    
    def __init__(self):
        super().__init__()
        
        # Patrones basados en el formato real
        self.patrones = {
            'numero': r'COMPROBANTE\s*DE\s*PERCEPCIÓN\s*ELECTRÓNICA\s*(P\d{3}\s*-\s*\d{8})',
            'serie': r'(P\d{3})',
            'ruc': r'R\.U\.C:\s*(\d{11})',
            'fecha_emision': r'Fecha\s*de\s*Emisión:\s*(\d{2}/\d{2}/\d{4})',
            'proveedor': r'(Natura Cosméticos S\.A\.)',
            'monto': r'Importe\s*Total\s*Percibido:\s*([\d,]+\.\d{2})',
            'factura_asociada': r'Factura\s*Electrónica\s*(F\d{3}-\d{8})',
        }
    
    def extraer(self, ruta_pdf: str) -> dict:
        """
        Extrae todos los datos de la percepción.
        """
        # Leer el PDF
        texto = self._leer_pdf(ruta_pdf)
        if not texto:
            return None
        
        datos = {}
        
        # 1. Extraer con patrones principales
        for campo, patron in self.patrones.items():
            # Usar self._buscar_patron correctamente
            valor = self._buscar_patron(patron)
            if valor:
                if campo == 'monto':
                    datos[campo] = self._limpiar_monto(valor)
                elif campo == 'fecha_emision':
                    fecha = self._extraer_fecha(patron)
                    if fecha:
                        datos[campo] = fecha
                else:
                    datos[campo] = valor.strip()
        
        # 2. Si no se encontró el número, extraer del nombre del archivo
        if 'numero' not in datos:
            nombre = Path(ruta_pdf).stem
            match = re.search(r'P\d{3}-\d{8}', nombre)
            if match:
                datos['numero'] = match.group(0)
            else:
                datos['numero'] = nombre[:15]
        
        # 3. Extraer serie
        if 'serie' not in datos and 'numero' in datos:
            match = re.search(r'(P\d{3})', datos['numero'])
            if match:
                datos['serie'] = match.group(1)
        
        # 4. RUC por defecto
        if 'ruc' not in datos:
            datos['ruc'] = '20101796532'
        
        # 5. Proveedor por defecto
        if 'proveedor' not in datos:
            datos['proveedor'] = 'NATURA COSMETICOS S.A.'
        
        # 6. Tipo
        datos['tipo'] = 'PERCEPCION'
        
        # 7. Observaciones
        observaciones = []
        if not datos.get('numero'):
            observaciones.append("Número de percepción no encontrado")
        if not datos.get('factura_asociada'):
            observaciones.append("Factura asociada no encontrada")
        if datos.get('monto', 0) == 0:
            observaciones.append("Monto percibido es 0 - verificar")
        
        datos['observaciones'] = ' | '.join(observaciones) if observaciones else 'OK'
        
        # 8. Agregar ruta del PDF
        datos['ruta_pdf'] = ruta_pdf
        
        return datos