# src/processors/procesador_pdfs.py
# =================================
# Procesador de archivos PDF para extracción de datos financieros.
# Soporte para: Facturas Natura, Boletas SUNAT, Percepciones.
# =================================

import re
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

import pdfplumber
from pdfplumber.page import Page

logger = logging.getLogger(__name__)


@dataclass
class DocumentoExtraido:
    """DTO para datos extraídos del PDF."""
    numero: str = ''
    tipo: str = ''  # factura, boleta, percepcion
    ruc_emisor: str = ''
    ruc_cliente: str = ''
    nombre_cliente: str = ''
    fecha_emision: str = ''
    monto_total: float = 0.0
    monto_base: float = 0.0
    percepcion: float = 0.0
    documento_asociado: str = ''
    archivo: str = ''
    fecha_procesamiento: datetime = field(default_factory=datetime.now)
    ciclo: str = ''
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para almacenamiento."""
        return {
            'numero': self.numero,
            'tipo': self.tipo,
            'ruc_emisor': self.ruc_emisor,
            'ruc_cliente': self.ruc_cliente,
            'nombre_cliente': self.nombre_cliente,
            'fecha_emision': self.fecha_emision,
            'monto_total': self.monto_total,
            'monto_base': self.monto_base,
            'percepcion': self.percepcion,
            'documento_asociado': self.documento_asociado,
            'archivo': self.archivo,
            'ciclo': self.ciclo,
            'fecha_procesamiento': self.fecha_procesamiento.isoformat()
        }


class PDFProcessor:
    """
    Clase principal para procesamiento de PDFs.
    """
    
    def __init__(self, file_path: Path):
        """
        Inicializa el procesador.
        
        Args:
            file_path: Ruta al archivo PDF
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        self._data: Optional[DocumentoExtraido] = None
        
    def process(self) -> DocumentoExtraido:
        """
        Procesa el PDF y extrae los datos.
        """
        try:
            with pdfplumber.open(self.file_path) as pdf:
                if not pdf.pages:
                    raise ValueError("PDF sin páginas")
                
                # Extraer texto de todas las páginas
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if not text:
                    raise ValueError("No se pudo extraer texto del PDF")
                
                # Determinar tipo de documento
                tipo = self._determinar_tipo(text)
                logger.info(f"Documento tipo: {tipo} - {self.file_path.name}")
                
                # Extraer datos según tipo
                if tipo == 'factura':
                    self._data = self._extraer_factura(text)
                elif tipo == 'boleta':
                    self._data = self._extraer_boleta(text)
                elif tipo == 'percepcion':
                    self._data = self._extraer_percepcion(text)
                else:
                    # Intentar extraer genérico
                    self._data = self._extraer_generico(text)
                
                self._data.archivo = self.file_path.name
                self._data.tipo = tipo
                
                logger.info(f"PDF procesado: {self.file_path.name}")
                return self._data
                
        except Exception as e:
            logger.error(f"Error procesando PDF {self.file_path}: {e}")
            raise
    
    def _determinar_tipo(self, text: str) -> str:
        """Determina el tipo de documento."""
        text_upper = text.upper()
        if 'FACTURA DE VENTA ELECTRÓNICA' in text_upper:
            return 'factura'
        elif 'BOLETA DE VENTA ELECTRONICA' in text_upper:
            return 'boleta'
        elif 'COMPROBANTE DE PERCEPCIÓN' in text_upper:
            return 'percepcion'
        else:
            return 'desconocido'
    
    def _extraer_factura(self, text: str) -> DocumentoExtraido:
        """Extrae datos de factura Natura."""
        data = DocumentoExtraido()
        
        # Número de factura
        num_match = re.search(r'N°?\s*([A-Z0-9\-]+)', text)
        if num_match:
            data.numero = num_match.group(1).strip()
        
        # RUC Emisor (Natura)
        ruc_match = re.search(r'R\.U\.C[:\s]*(\d{11})', text)
        if ruc_match:
            data.ruc_emisor = ruc_match.group(1)
        
        # RUC Cliente
        ruc_cli_match = re.search(r'RUC[:\s]*(\d{11})', text)
        if ruc_cli_match:
            data.ruc_cliente = ruc_cli_match.group(1)
        
        # Nombre Cliente
        nombre_match = re.search(r'Nombre CB[:\s]*([^\n]+)', text)
        if nombre_match:
            data.nombre_cliente = nombre_match.group(1).strip()
        
        # Fecha de emisión
        fecha_match = re.search(r'Fecha Emisión[:\s]*(\d{1,2}/\d{1,2}/\d{4})', text)
        if fecha_match:
            data.fecha_emision = fecha_match.group(1)
        
        # Ciclo
        ciclo_match = re.search(r'Ciclo[:\s]*(\d{6})', text)
        if ciclo_match:
            data.ciclo = ciclo_match.group(1)
        
        # Total con descuento (A)
        total_match = re.search(r'\(A\)\s*Total con Dscto[.:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if total_match:
            data.monto_total = self._parse_monto(total_match.group(1))
        
        # Si no encuentra (A), buscar otro patrón
        if data.monto_total == 0:
            total_match2 = re.search(r'Total a Pagar[:\s]*S/?\s*([\d,]+\.?\d*)', text)
            if total_match2:
                data.monto_total = self._parse_monto(total_match2.group(1))
        
        # Percepción (B)
        perc_match = re.search(r'\(B\)\s*Percepción[.\s]*S/?\s*([\d,]+\.?\d*)', text)
        if perc_match:
            data.percepcion = self._parse_monto(perc_match.group(1))
        
        # Base (Sub Total)
        base_match = re.search(r'Sub Total[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if base_match:
            data.monto_base = self._parse_monto(base_match.group(1))
        
        return data
    
    def _extraer_boleta(self, text: str) -> DocumentoExtraido:
        """Extrae datos de boleta SUNAT."""
        data = DocumentoExtraido()
        
        # Número de boleta
        num_match = re.search(r'BOLETA.*?N°?\s*([A-Z0-9\-]+)', text)
        if not num_match:
            num_match = re.search(r'N°?\s*([A-Z0-9\-]+)', text)
        if num_match:
            data.numero = num_match.group(1).strip()
        
        # RUC Emisor (Doña María)
        ruc_match = re.search(r'RUC[:\s]*(\d{11})', text)
        if ruc_match:
            data.ruc_emisor = ruc_match.group(1)
        
        # Nombre Cliente (Señor(es))
        nombre_match = re.search(r'Señor\(es\)[:\s]*([^\n]+)', text)
        if not nombre_match:
            nombre_match = re.search(r'Cliente[:\s]*([^\n]+)', text)
        if nombre_match:
            data.nombre_cliente = nombre_match.group(1).strip()
        
        # Fecha de emisión
        fecha_match = re.search(r'Fecha de Emisión[:\s]*(\d{1,2}/\d{1,2}/\d{4})', text)
        if fecha_match:
            data.fecha_emision = fecha_match.group(1)
        
        # Importe Total
        total_match = re.search(r'Importe Total[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if total_match:
            data.monto_total = self._parse_monto(total_match.group(1))
        else:
            # Buscar al final del texto
            total_match2 = re.search(r'S/?\s*([\d,]+\.?\d*)\s*$', text)
            if total_match2:
                data.monto_total = self._parse_monto(total_match2.group(1))
        
        return data
    
    def _extraer_percepcion(self, text: str) -> DocumentoExtraido:
        """Extrae datos de comprobante de percepción."""
        data = DocumentoExtraido()
        
        # Número de percepción
        num_match = re.search(r'P\d{3}\s*-\s*(\d+)', text)
        if not num_match:
            num_match = re.search(r'N°?\s*([A-Z0-9\-]+)', text)
        if num_match:
            data.numero = num_match.group(0).strip()
        
        # RUC Emisor
        ruc_match = re.search(r'R\.U\.C[:\s]*(\d{11})', text)
        if ruc_match:
            data.ruc_emisor = ruc_match.group(1)
        
        # RUC Cliente
        ruc_cli_match = re.search(r'RUC[:\s]*(\d{11})', text)
        if ruc_cli_match:
            data.ruc_cliente = ruc_cli_match.group(1)
        
        # Nombre Cliente
        nombre_match = re.search(r'Señor\(es\)[:\s]*([^\n]+)', text)
        if nombre_match:
            data.nombre_cliente = nombre_match.group(1).strip()
        
        # Fecha de emisión
        fecha_match = re.search(r'Fecha de Emisión[:\s]*(\d{1,2}/\d{1,2}/\d{4})', text)
        if fecha_match:
            data.fecha_emision = fecha_match.group(1)
        
        # Documento asociado (Factura)
        factura_match = re.search(r'Factura\s+Electrónica\s+([A-Z0-9\-]+)', text)
        if factura_match:
            data.documento_asociado = factura_match.group(1)
        
        # Importe Total Percibido
        perc_match = re.search(r'Importe Total Percibido[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if perc_match:
            data.percepcion = self._parse_monto(perc_match.group(1))
            data.monto_total = data.percepcion
        
        # Base
        base_match = re.search(r'BASE[:\s]*S/?\s*([\d,]+\.?\d*)', text)
        if base_match:
            data.monto_base = self._parse_monto(base_match.group(1))
        
        return data
    
    def _extraer_generico(self, text: str) -> DocumentoExtraido:
        """Extrae datos de manera genérica."""
        data = DocumentoExtraido()
        
        # Buscar números de documento
        num_match = re.search(r'N°?\s*([A-Z0-9\-]+)', text)
        if num_match:
            data.numero = num_match.group(1).strip()
        
        # Buscar RUCs
        rucs = re.findall(r'(\d{11})', text)
        if len(rucs) >= 2:
            data.ruc_emisor = rucs[0]
            data.ruc_cliente = rucs[1]
        elif rucs:
            data.ruc_emisor = rucs[0]
        
        # Buscar fechas
        fechas = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', text)
        if fechas:
            data.fecha_emision = fechas[0]
        
        # Buscar monto total (último número con S/)
        montos = re.findall(r'S/?\s*([\d,]+\.?\d*)', text)
        if montos:
            data.monto_total = self._parse_monto(montos[-1])
        
        return data
    
    def _parse_monto(self, value: str) -> float:
        """Convierte string de monto a float."""
        try:
            # Limpiar: remover puntos de miles y reemplazar coma decimal
            cleaned = value.replace('.', '').replace(',', '.')
            # Remover cualquier caracter no numérico excepto punto
            cleaned = re.sub(r'[^\d.]', '', cleaned)
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0.0


class ProcesadorPDFs:
    """
    Clase principal para procesamiento de PDFs.
    """
    
    @staticmethod
    def procesar(archivo_path: Path) -> Dict[str, Any]:
        """
        Procesa un archivo PDF.
        
        Args:
            archivo_path: Ruta al archivo PDF
            
        Returns:
            Dict: Datos extraídos
        """
        processor = PDFProcessor(archivo_path)
        data = processor.process()
        return data.to_dict()
    
    @staticmethod
    def procesar_multiples(archivos: List[Path]) -> List[Dict[str, Any]]:
        """
        Procesa múltiples archivos PDF.
        
        Args:
            archivos: Lista de rutas a archivos PDF
            
        Returns:
            List[Dict]: Lista de datos extraídos
        """
        resultados = []
        for archivo in archivos:
            try:
                resultado = ProcesadorPDFs.procesar(archivo)
                resultados.append(resultado)
            except Exception as e:
                logger.error(f"Error procesando {archivo}: {e}")
                # Continuar con el siguiente archivo
        return resultados
