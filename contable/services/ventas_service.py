# src/services/ventas_service.py
# ==============================
# Servicio de gestión de ventas y cálculos RUS.

import logging
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from pathlib import Path

from sqlalchemy import func
from src.database.conexion import db
from src.database.models import Documento, Historial
from src.processors.procesador_pdfs import ProcesadorPDFs

logger = logging.getLogger(__name__)


class VentasService:
    """
    Servicio para gestión de ventas y cálculos financieros.
    """
    
    def __init__(self):
        self.limite_rus = 8000
        self.impuesto_normal = 20.00
        self.impuesto_alerta = 50.00
    
    def get_resumen_mensual(self, year: int, month: int) -> Dict[str, Any]:
        """Obtiene el resumen financiero para un mes específico."""
        try:
            fecha_inicio = date(year, month, 1)
            if month == 12:
                fecha_fin = date(year + 1, 1, 1)
            else:
                fecha_fin = date(year, month + 1, 1)
            
            # Ventas (boletas)
            ventas = db.session.query(func.sum(Documento.monto_total))\
                .filter(Documento.tipo == 'boleta')\
                .filter(Documento.fecha_emision >= fecha_inicio)\
                .filter(Documento.fecha_emision < fecha_fin)\
                .scalar() or 0
            
            # Compras (facturas)
            compras = db.session.query(func.sum(Documento.monto_total))\
                .filter(Documento.tipo == 'factura')\
                .filter(Documento.fecha_emision >= fecha_inicio)\
                .filter(Documento.fecha_emision < fecha_fin)\
                .scalar() or 0
            
            # Percepciones
            percepciones = db.session.query(func.sum(Documento.percepcion))\
                .filter(Documento.tipo == 'percepcion')\
                .filter(Documento.fecha_emision >= fecha_inicio)\
                .filter(Documento.fecha_emision < fecha_fin)\
                .scalar() or 0
            
            total_docs = db.session.query(Documento)\
                .filter(Documento.fecha_emision >= fecha_inicio)\
                .filter(Documento.fecha_emision < fecha_fin)\
                .count()
            
            utilidad = ventas - compras
            estado_rus = self._calcular_estado_rus(ventas)
            
            return {
                'ventas': float(ventas),
                'compras': float(compras),
                'utilidad': float(utilidad),
                'percepciones': float(percepciones),
                'total_documentos': total_docs,
                'estado_rus': estado_rus,
                'mes': f"{year}-{month:02d}"
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo resumen mensual: {e}")
            return {
                'ventas': 0,
                'compras': 0,
                'utilidad': 0,
                'percepciones': 0,
                'total_documentos': 0,
                'estado_rus': {'estado': 'ERROR', 'mensaje': 'Error al calcular'},
                'mes': f"{year}-{month:02d}"
            }
    
    def get_variacion_mensual(self, year: int, month: int) -> Dict[str, float]:
        """Calcula la variación vs mes anterior."""
        try:
            actual = self.get_resumen_mensual(year, month)
            mes_ant, year_ant = self._get_mes_anterior(year, month)
            anterior = self.get_resumen_mensual(year_ant, mes_ant)
            
            def calc_variacion(actual_val, anterior_val):
                if anterior_val == 0:
                    return 0
                return ((actual_val - anterior_val) / anterior_val) * 100
            
            return {
                'ventas': calc_variacion(actual['ventas'], anterior['ventas']),
                'compras': calc_variacion(actual['compras'], anterior['compras']),
                'utilidad': calc_variacion(actual['utilidad'], anterior['utilidad'])
            }
            
        except Exception as e:
            logger.error(f"Error calculando variación: {e}")
            return {'ventas': 0, 'compras': 0, 'utilidad': 0}
    
    def get_ultimos_documentos(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtiene los últimos documentos procesados."""
        try:
            documentos = Documento.query\
                .order_by(Documento.fecha_procesamiento.desc())\
                .limit(limit)\
                .all()
            return [doc.to_dict() for doc in documentos]
        except Exception as e:
            logger.error(f"Error obteniendo últimos documentos: {e}")
            return []
    
    def get_documentos_mes(self, year: int, month: int) -> List[Dict[str, Any]]:
        """Obtiene todos los documentos de un mes."""
        try:
            fecha_inicio = date(year, month, 1)
            if month == 12:
                fecha_fin = date(year + 1, 1, 1)
            else:
                fecha_fin = date(year, month + 1, 1)
            
            documentos = Documento.query\
                .filter(Documento.fecha_emision >= fecha_inicio)\
                .filter(Documento.fecha_emision < fecha_fin)\
                .order_by(Documento.fecha_emision.desc())\
                .all()
            return [doc.to_dict() for doc in documentos]
            
        except Exception as e:
            logger.error(f"Error obteniendo documentos del mes: {e}")
            return []
    
    def procesar_archivo(self, file_path: Path) -> Dict[str, Any]:
        """Procesa un archivo PDF y lo guarda en la base de datos."""
        try:
            data = ProcesadorPDFs.procesar(file_path)
            
            existing = Documento.query.filter_by(numero=data['numero']).first()
            if existing:
                return {
                    'success': False,
                    'message': f'Documento {data["numero"]} ya existe',
                    'data': data
                }
            
            documento = Documento(
                numero=data['numero'],
                tipo=data['tipo'],
                ruc_emisor=data.get('ruc_emisor', ''),
                ruc_cliente=data.get('ruc_cliente', ''),
                nombre_cliente=data.get('nombre_cliente', ''),
                fecha_emision=datetime.strptime(data['fecha_emision'], '%d/%m/%Y').date() if data.get('fecha_emision') else date.today(),
                monto_total=data['monto_total'],
                monto_base=data.get('monto_base', 0),
                percepcion=data.get('percepcion', 0),
                archivo_original=data['archivo'],
                documento_asociado=data.get('documento_asociado', ''),
                ciclo=data.get('ciclo', '')
            )
            
            db.session.add(documento)
            db.session.commit()
            
            Historial.registrar(
                'upload',
                f'Documento {data["numero"]} ({data["tipo"]}) - S/{data["monto_total"]:.2f}'
            )
            
            logger.info(f"Documento guardado: {data['numero']}")
            
            return {
                'success': True,
                'message': f'Documento {data["numero"]} procesado correctamente',
                'data': data
            }
            
        except Exception as e:
            logger.error(f"Error procesando archivo: {e}")
            return {
                'success': False,
                'message': f'Error al procesar: {str(e)}',
                'data': None
            }
    
    def _calcular_estado_rus(self, total_ventas: float) -> Dict[str, Any]:
        """Calcula el estado RUS basado en ventas mensuales."""
        if total_ventas < 5000:
            return {
                'estado': 'NORMAL',
                'impuesto': 20.00,
                'mensaje': '✅ Todo bien, sigue así',
                'color': 'green',
                'icon': '✅'
            }
        elif total_ventas <= self.limite_rus:
            return {
                'estado': 'ALERTA',
                'impuesto': 50.00,
                'mensaje': f'⚠️ Estás cerca del límite (S/{self.limite_rus})',
                'color': 'orange',
                'icon': '⚠️'
            }
        else:
            return {
                'estado': 'URGENTE',
                'impuesto': 0,
                'mensaje': '🚨 ¡EXCEDISTE EL LÍMITE! Contacta a tu contador',
                'color': 'red',
                'icon': '🚨'
            }
    
    def _get_mes_anterior(self, year: int, month: int) -> tuple:
        """Obtiene el mes anterior."""
        if month == 1:
            return 12, year - 1
        return month - 1, year
    
    def cargar_datos_prueba(self) -> Dict[str, Any]:
        """Carga datos de prueba desde archivos PDF."""
        resultados = {
            'procesados': 0,
            'errores': 0,
            'documentos': []
        }
        
        # Buscar archivos en data/
        pdf_files = list(Path("data").glob("**/*.pdf"))
        
        for file_path in pdf_files:
            try:
                result = self.procesar_archivo(file_path)
                if result['success']:
                    resultados['procesados'] += 1
                    resultados['documentos'].append(result['data'])
                else:
                    resultados['errores'] += 1
            except Exception as e:
                logger.error(f"Error cargando {file_path}: {e}")
                resultados['errores'] += 1
        
        return resultados
