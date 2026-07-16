"""
EXTRACTOR BASE - VERSIÓN MEJORADA CON DETECCIÓN AUTOMÁTICA
Clase base para todos los extractores de PDF
"""
import pdfplumber
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

class BaseExtractor(ABC):
    """Clase base abstracta para todos los extractores de PDF"""

    def __init__(self):
        self.texto = ""
        self.patrones = {}

    @abstractmethod
    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """Método abstracto que debe ser implementado por cada extractor"""
        pass

    def extraer_texto(self, ruta_pdf: str) -> Optional[str]:
        """Lee el PDF y guarda el texto completo"""
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                texto_completo = ""
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo += texto + "\n"
                self.texto = texto_completo
                return self.texto
        except Exception as e:
            print(f"❌ Error al leer PDF: {e}")
            return None

    def buscar_patron(self, patron: str) -> Optional[str]:
        """Busca un patrón en el texto y devuelve el primer grupo"""
        try:
            match = re.search(patron, self.texto, re.IGNORECASE)
            if match:
                if match.groups():
                    return match.group(1).strip()
                return match.group(0).strip()
            return None
        except Exception as e:
            print(f"❌ Error al buscar patrón: {e}")
            return None

    def extraer_fecha(self, patron: str) -> Optional[str]:
        """Extrae una fecha en formato DD/MM/YYYY"""
        fecha_str = self.buscar_patron(patron)
        if fecha_str:
            try:
                for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']:
                    try:
                        fecha = datetime.strptime(fecha_str, fmt)
                        return fecha.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            except Exception:
                pass
        return None

    # ============================================================
    # DETECCIÓN AUTOMÁTICA DE FECHA (MES Y AÑO)
    # ============================================================

    def detectar_fecha_emision(self) -> Optional[Tuple[int, int]]:
        """
        Detecta automáticamente la fecha de emisión del documento.
        Retorna: (mes, año) o None si no se pudo detectar.
        """
        if not self.texto:
            return None

        # ============================================================
        # PATRONES DE FECHA COMUNES
        # ============================================================
        patrones_fecha = [
            # Formato: Fecha Emisión: 08/05/2026
            r'fecha\s*emisi[oó]n\s*[:]?\s*(\d{2})[/.-](\d{2})[/.-](\d{4})',
            # Formato: Fecha de Emisión : 31/05/2026
            r'fecha\s*de\s*emisi[oó]n\s*[:]?\s*(\d{2})[/.-](\d{2})[/.-](\d{4})',
            # Formato: FECHA: 08/05/2026
            r'fecha\s*[:]?\s*(\d{2})[/.-](\d{2})[/.-](\d{4})',
            # Formato: 08/05/2026 (suelto)
            r'(\d{2})[/.-](\d{2})[/.-](\d{4})',
        ]

        for patron in patrones_fecha:
            match = re.search(patron, self.texto, re.IGNORECASE)
            if match:
                try:
                    dia = int(match.group(1))
                    mes = int(match.group(2))
                    anio = int(match.group(3))

                    # Validar que la fecha sea razonable
                    if 1 <= mes <= 12 and 1 <= dia <= 31 and 2000 <= anio <= 2030:
                        return (mes, anio)
                except (ValueError, IndexError):
                    continue

        # ============================================================
        # SI NO SE ENCUENTRA FECHA, USAR LA FECHA ACTUAL
        # ============================================================
        hoy = datetime.now()
        return (hoy.month, hoy.year)

    # ============================================================
    # DETECCIÓN AUTOMÁTICA DE TIPO DE DOCUMENTO
    # ============================================================

    def detectar_tipo_documento(self) -> str:
        """
        Detecta automáticamente el tipo de documento analizando el texto.
        Retorna: 'factura', 'boleta', 'percepcion' o 'desconocido'
        """
        if not self.texto:
            return 'desconocido'

        texto_lower = self.texto.lower()

        # Detectar Boleta
        patrones_boleta = [
            r'boleta\s*de\s*venta\s*electronica',
            r'boleta\s*electronica',
            r'eb\d{2}-\d{3,6}',
            r'ruc\s*[:]?\s*\d{11}\s*eb\d{2}',
        ]
        for patron in patrones_boleta:
            if re.search(patron, texto_lower):
                return 'boleta'

        # Detectar Percepción
        patrones_percepcion = [
            r'comprobante\s*de\s*percepci[oó]n',
            r'p\d{3}\s*-\s*006\d{4,8}',
        ]
        for patron in patrones_percepcion:
            if re.search(patron, texto_lower):
                return 'percepcion'


        # Detectar Factura
        patrones_factura = [
            r'factura\s*de\s*venta\s*electronica',
            r'factura\s*electronica',
            r'f\d{3}\s*[-]\s*\d{3,8}',
            r'f\d{3}\s*\d{3,8}',
        ]
        for patron in patrones_factura:
            if re.search(patron, texto_lower):
                return 'factura'

        # Detectar por contenido específico
        if re.search(r'r\.u\.c', texto_lower) and re.search(r'factura', texto_lower):
            return 'factura'
        if re.search(r'ruc\s*[:]?\s*\d{11}', texto_lower) and re.search(r'boleta', texto_lower):
            return 'boleta'

        return 'desconocido'

    def obtener_recomendacion_tipo(self) -> Tuple[str, str]:
        """
        Detecta el tipo real del documento y devuelve una tupla:
        (tipo_detectado, mensaje_para_usuario)
        """
        tipo_real = self.detectar_tipo_documento()

        mensajes = {
            'factura': '📄 Este PDF parece ser una Factura',
            'boleta': '🧾 Este PDF parece ser una Boleta',
            'percepcion': '💰 Este PDF parece ser una Percepción',
            'desconocido': '⚠️ No se pudo determinar el tipo de documento'
        }

        return tipo_real, mensajes.get(tipo_real, mensajes['desconocido'])

    def obtener_recomendacion_fecha(self) -> Tuple[Optional[int], Optional[int], str]:
        """
        Detecta la fecha real del documento y devuelve:
        (mes_detectado, año_detectado, mensaje_para_usuario)
        """
        fecha = self.detectar_fecha_emision()
        if fecha:
            mes, anio = fecha
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            mensaje = f"📅 Fecha detectada: {meses[mes-1]} {anio}"
            return (mes, anio, mensaje)
        else:
            return (None, None, "⚠️ No se pudo detectar la fecha, se usará la seleccionada")