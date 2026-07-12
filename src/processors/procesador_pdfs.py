# src/processors/procesador_pdfs.py
"""
🔄 PROCESADOR AUTOMÁTICO DE PDFS
Usa repositorios para guardar los datos
"""

import sys
from pathlib import Path
from datetime import datetime
import re

sys.path.append(str(Path(__file__).parent.parent))

from src.extractors.extractor_factura import ExtractorFacturaNatura
from src.extractors.extractor_boleta import ExtractorBoleta
from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository

class ProcesadorPDF:
    """Procesa PDFs automáticamente usando repositorios"""
    
    def __init__(self):
        self.extractor_factura = ExtractorFacturaNatura()
        self.extractor_boleta = ExtractorBoleta()
        self.repo_factura = FacturaRepository()
        self.repo_boleta = BoletaRepository()
        self.repo_percepcion = PercepcionRepository()
        self.resultados = {
            'exitosos': [],
            'fallidos': [],
            'totales': 0
        }
    
    def procesar_archivo(self, ruta_pdf, tipo_documento, mes, año):
        """Procesa un archivo PDF según su tipo"""
        self.resultados['totales'] += 1
        ruta = Path(ruta_pdf)
        
        try:
            if tipo_documento == "facturas":
                return self._procesar_factura(ruta, mes, año)
            elif tipo_documento == "boletas":
                return self._procesar_boleta(ruta, mes, año)
            elif tipo_documento == "percepciones":
                return self._procesar_percepcion(ruta, mes, año)
            else:
                raise ValueError(f"Tipo no soportado: {tipo_documento}")
        
        except Exception as e:
            error_msg = f"❌ Error en {ruta.name}: {str(e)}"
            self.resultados['fallidos'].append(error_msg)
            return {'exito': False, 'error': error_msg}
    
    def _procesar_factura(self, ruta, mes, año):
        """Procesa una factura usando el repositorio"""
        datos = self.extractor_factura.extraer(str(ruta))
        
        if not datos:
            return {'exito': False, 'error': 'No se pudieron extraer los datos'}
        
        # Agregar metadatos
        datos['ruta_pdf'] = str(ruta)
        datos['fecha_subida'] = datetime.now()
        datos['estado'] = 'procesado'
        
        if not datos.get('numero_factura'):
            datos['numero_factura'] = ruta.stem[:15]
        
        # Verificar si ya existe
        if self.repo_factura.existe_numero(datos['numero_factura']):
            self.resultados['exitosos'].append({
                'tipo': 'factura',
                'numero': datos['numero_factura'],
                'ruta': str(ruta),
                'monto': datos.get('total_pagar', 0),
                'duplicado': True
            })
            return {'exito': True, 'mensaje': 'Factura ya existente', 'duplicado': True}
        
        try:
            factura = self.repo_factura.guardar(datos)
            self.resultados['exitosos'].append({
                'tipo': 'factura',
                'numero': factura.numero_factura,
                'ruta': str(ruta),
                'monto': factura.total_pagar
            })
            return {'exito': True, 'datos': datos, 'factura': factura}
        except Exception as e:
            return {'exito': False, 'error': str(e)}
    
    def _procesar_boleta(self, ruta, mes, año):
        """Procesa una boleta usando el repositorio"""
        datos = self.extractor_boleta.extraer(str(ruta))
        
        if not datos:
            return {'exito': False, 'error': 'No se pudieron extraer los datos'}
        
        datos['ruta_pdf'] = str(ruta)
        datos['fecha_subida'] = datetime.now()
        datos['estado'] = 'procesado'
        
        if not datos.get('numero_boleta'):
            datos['numero_boleta'] = ruta.stem[:15]
        
        if self.repo_boleta.existe_numero(datos['numero_boleta']):
            self.resultados['exitosos'].append({
                'tipo': 'boleta',
                'numero': datos['numero_boleta'],
                'ruta': str(ruta),
                'monto': datos.get('monto_total', 0),
                'duplicado': True
            })
            return {'exito': True, 'mensaje': 'Boleta ya existente', 'duplicado': True}
        
        try:
            boleta = self.repo_boleta.guardar(datos)
            self.resultados['exitosos'].append({
                'tipo': 'boleta',
                'numero': boleta.numero_boleta,
                'ruta': str(ruta),
                'monto': boleta.monto_total
            })
            return {'exito': True, 'datos': datos, 'boleta': boleta}
        except Exception as e:
            return {'exito': False, 'error': str(e)}
    
    def _procesar_percepcion(self, ruta, mes, año):
        """Procesa una percepción usando el repositorio"""
        nombre = ruta.stem
        patron = r'(\d{11})-P(\d{3})-\d{8}'
        match = re.search(patron, nombre)
        
        datos = {
            'numero_doc': f"P{nombre[-8:]}",
            'fecha_emision': datetime(año, mes, 1).date(),
            'proveedor': 'NATURA COSMETICOS S.A.',
            'monto': 0.0,
            'ruta_pdf': str(ruta),
            'fecha_subida': datetime.now()
        }
        
        if match:
            datos['ruc_proveedor'] = match.group(1)
        
        try:
            percepcion = self.repo_percepcion.guardar(datos)
            self.resultados['exitosos'].append({
                'tipo': 'percepcion',
                'numero': percepcion.numero_doc,
                'ruta': str(ruta)
            })
            return {'exito': True, 'datos': datos, 'percepcion': percepcion}
        except Exception as e:
            return {'exito': False, 'error': str(e)}
    
    def obtener_resumen(self):
        """Obtiene un resumen del procesamiento"""
        return {
            'total': self.resultados['totales'],
            'exitosos': len(self.resultados['exitosos']),
            'fallidos': len(self.resultados['fallidos']),
            'detalle_exitosos': self.resultados['exitosos'],
            'detalle_fallidos': self.resultados['fallidos']
        }
    
    def cerrar_conexiones(self):
        """Cierra todas las conexiones a la base de datos"""
        self.repo_factura.close()
        self.repo_boleta.close()
        self.repo_percepcion.close()