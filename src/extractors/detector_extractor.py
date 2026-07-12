"""
EXTRACTOR DETECTOR - Para análisis rápido de PDFs sin procesar datos completos
"""
from src.extractors.base_extractor import BaseExtractor
from typing import Dict, Any

class DetectorExtractor(BaseExtractor):
    """
    Extractor especializado solo para detectar tipo y fecha de un PDF.
    No extrae datos completos, solo analiza el texto.
    """
    
    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """
        Implementación requerida por la clase abstracta.
        Solo lee el texto y devuelve un diccionario básico con la detección.
        """
        # Leer el texto del PDF
        self.extraer_texto(ruta_pdf)
        
        # Detectar tipo y fecha
        tipo = self.detectar_tipo_documento()
        fecha = self.detectar_fecha_emision()
        
        return {
            'tipo_detectado': tipo,
            'fecha_detectada': fecha,
            'texto_longitud': len(self.texto) if self.texto else 0
        }