"""
Servicio para la gestión de documentos financieros
Centraliza la lógica de negocio relacionada con documentos
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository
from src.extractors import DetectorExtractor, FacturaExtractor, BoletaExtractor, PercepcionExtractor
from src.database.conexion import get_db
from src.utils.notificador import Notificador
import os
from werkzeug.utils import secure_filename

class DocumentoService:
    """Servicio para operaciones con documentos financieros"""
    
    def __init__(self):
        self.session = get_db()
        self.factura_repo = FacturaRepository(self.session)
        self.boleta_repo = BoletaRepository(self.session)
        self.percepcion_repo = PercepcionRepository(self.session)
    
    def procesar_documento(self, archivo, tipo_seleccionado: str, mes_seleccionado: int, anio_seleccionado: int) -> Tuple[Dict, List[str]]:
        """
        Procesa un documento PDF: detecta tipo, fecha, extrae datos y guarda
        
        Returns:
            (resultado, advertencias)
        """
        advertencias = []
        
        # 1. Guardar temporalmente
        filename = secure_filename(archivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_guardado = f"{timestamp}_{filename}"
        
        # 2. Detectar tipo y fecha
        detector = DetectorExtractor()
        resultado_deteccion = detector.extraer(archivo)
        
        tipo_real = resultado_deteccion.get('tipo_detectado', 'desconocido')
        fecha_detectada = resultado_deteccion.get('fecha_detectada')
        
        # 3. Decidir tipo y fecha a usar
        if tipo_real == 'desconocido':
            tipo_usar = tipo_seleccionado
            advertencias.append(f"⚠️ No se pudo detectar el tipo de '{archivo.filename}'. Se usará '{tipo_seleccionado}'.")
        else:
            tipo_usar = tipo_real
            if tipo_real != tipo_seleccionado:
                advertencias.append(f"🔍 Detectamos que '{archivo.filename}' es una {tipo_real}.")
        
        if fecha_detectada:
            mes_usar, anio_usar = fecha_detectada
            if mes_usar != mes_seleccionado or anio_usar != anio_seleccionado:
                meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                advertencias.append(
                    f"📅 Detectamos que '{archivo.filename}' es de {meses[mes_usar-1]} {anio_usar}."
                )
        else:
            mes_usar = mes_seleccionado
            anio_usar = anio_seleccionado
        
        # 4. Procesar con el extractor correcto
        resultado = self._procesar_con_extractor(tipo_usar, archivo, mes_usar, anio_usar)
        
        return resultado, advertencias
    
    def _procesar_con_extractor(self, tipo: str, archivo, mes: int, anio: int) -> Dict:
        """Procesa el archivo con el extractor correspondiente"""
        # Implementación específica para cada tipo
        # (Este método encapsula la lógica que antes estaba en routes.py)
        pass
    
    def obtener_estadisticas(self, mes: int, anio: int) -> Dict[str, Any]:
        """Obtiene estadísticas consolidadas para un mes/año"""
        facturas = self.factura_repo.obtener_por_mes_anio(mes, anio)
        boletas = self.boleta_repo.obtener_por_mes_anio(mes, anio)
        percepciones = self.percepcion_repo.obtener_por_mes_anio(mes, anio)
        
        return {
            'facturas': facturas,
            'boletas': boletas,
            'percepciones': percepciones,
            'total_ventas': sum(b.total_pagar or 0 for b in boletas) if boletas else 0,
            'total_compras': sum(f.total_pagar or 0 for f in facturas) if facturas else 0,
            'total_percepciones': sum(p.monto or 0 for p in percepciones) if percepciones else 0,
            'total_documentos': len(facturas) + len(boletas) + len(percepciones)
        }
    
    def close(self):
        """Cierra la sesión de base de datos"""
        if self.session:
            self.session.close()