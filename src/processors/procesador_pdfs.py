# src/processors/procesador_pdfs.py
"""
⚙️ PROCESADOR PDF - VERSIÓN CORREGIDA
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from src.extractors.extractor_factura import ExtractorFacturaNatura
from src.extractors.extractor_boleta import ExtractorBoleta
from src.extractors.extractor_percepcion import ExtractorPercepcion
from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository
from src.database.conexion import get_db
from src.utils.gestor_carpetas import GestorCarpetas

class ProcesadorPDFs:
    """Procesador automático de PDFs"""

    def __init__(self):
        self.session = get_db()
        self.factura_repo = FacturaRepository(self.session)
        self.boleta_repo = BoletaRepository(self.session)
        self.percepcion_repo = PercepcionRepository(self.session)
        self.gestor = GestorCarpetas()

    def procesar_pdf(self, ruta_pdf: str, tipo: str = 'auto') -> Dict[str, Any]:
        resultado = {'exito': False, 'mensaje': '', 'datos': None, 'tipo': tipo}

        try:
            if not os.path.exists(ruta_pdf):
                resultado['mensaje'] = f"Archivo no encontrado: {ruta_pdf}"
                return resultado

            if tipo == 'auto':
                tipo = self._detectar_tipo(ruta_pdf)

            fecha_actual = datetime.now()
            carpeta_destino = self.gestor.crear_carpeta_mes(
                tipo, fecha_actual.month, fecha_actual.year
            )

            nombre_archivo = os.path.basename(ruta_pdf)
            ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
            shutil.copy2(ruta_pdf, ruta_destino)

            if tipo == 'factura':
                resultado = self._procesar_factura(ruta_destino)
            elif tipo == 'boleta':
                resultado = self._procesar_boleta(ruta_destino)
            elif tipo == 'percepcion':
                resultado = self._procesar_percepcion(ruta_destino)
            else:
                resultado['mensaje'] = f"Tipo no soportado: {tipo}"
                return resultado

            resultado['exito'] = True
            resultado['tipo'] = tipo
            return resultado

        except Exception as e:
            resultado['mensaje'] = f"Error al procesar: {str(e)}"
            return resultado

    def _detectar_tipo(self, ruta_pdf: str) -> str:
        try:
            extractor = ExtractorFacturaNatura()
            datos = extractor.extraer(ruta_pdf)
            if datos.get('numero_factura') and datos.get('total_pagar', 0) > 0:
                return 'factura'
        except:
            pass

        try:
            extractor = ExtractorBoleta()
            datos = extractor.extraer(ruta_pdf)
            if datos.get('numero_boleta') and datos.get('total_pagar', 0) > 0:
                return 'boleta'
        except:
            pass

        try:
            extractor = ExtractorPercepcion()
            datos = extractor.extraer(ruta_pdf)
            if datos.get('numero_comprobante') and datos.get('monto', 0) > 0:
                return 'percepcion'
        except:
            pass

        return 'desconocido'

    def _procesar_factura(self, ruta_pdf: str) -> Dict[str, Any]:
        try:
            extractor = ExtractorFacturaNatura()
            datos = extractor.extraer(ruta_pdf)
            datos['ruta_pdf'] = ruta_pdf
            
            # ⭐ Asegurar que "anio" esté presente
            if 'anio' not in datos:
                datos['anio'] = datetime.now().year
            
            existente = self.factura_repo.obtener_por_numero(
                datos.get('numero_factura', '')
            )

            if existente:
                return {
                    'mensaje': f"Factura {datos['numero_factura']} ya existe",
                    'datos': datos
                }

            factura = self.factura_repo.crear(**datos)
            return {
                'mensaje': f"Factura {datos['numero_factura']} procesada",
                'datos': datos,
                'id': factura.id
            }
        except Exception as e:
            return {'mensaje': f"Error: {str(e)}", 'datos': None}

    def _procesar_boleta(self, ruta_pdf: str) -> Dict[str, Any]:
        try:
            extractor = ExtractorBoleta()
            datos = extractor.extraer(ruta_pdf)
            datos['ruta_pdf'] = ruta_pdf
            
            # ⭐ Asegurar que "anio" esté presente
            if 'anio' not in datos:
                datos['anio'] = datetime.now().year

            existente = self.boleta_repo.obtener_por_numero(
                datos.get('numero_boleta', '')
            )

            if existente:
                return {
                    'mensaje': f"Boleta {datos['numero_boleta']} ya existe",
                    'datos': datos
                }

            boleta = self.boleta_repo.crear(**datos)
            return {
                'mensaje': f"Boleta {datos['numero_boleta']} procesada",
                'datos': datos,
                'id': boleta.id
            }
        except Exception as e:
            return {'mensaje': f"Error: {str(e)}", 'datos': None}

    def _procesar_percepcion(self, ruta_pdf: str) -> Dict[str, Any]:
        try:
            extractor = ExtractorPercepcion()
            datos = extractor.extraer(ruta_pdf)
            datos['ruta_pdf'] = ruta_pdf
            
            # ⭐ Asegurar que "anio" esté presente
            if 'anio' not in datos:
                datos['anio'] = datetime.now().year

            percepcion = self.percepcion_repo.crear(**datos)
            return {
                'mensaje': f"Percepción {datos['numero_comprobante']} procesada",
                'datos': datos,
                'id': percepcion.id
            }
        except Exception as e:
            return {'mensaje': f"Error: {str(e)}", 'datos': None}

    def close(self):
        if self.session:
            self.session.close()