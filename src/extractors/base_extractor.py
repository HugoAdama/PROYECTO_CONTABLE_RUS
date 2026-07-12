# src/extractors/base_extractor.py
"""
📄 EXTRACTOR BASE - VERSIÓN MEJORADA
Clase base para todos los extractores de PDF
"""

import pdfplumber
import re
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List

class ExtractorBase(ABC):
    """
    Clase base abstracta para todos los extractores de PDF.
    """
    
    def __init__(self):
        self.texto = ""
        self.patrones = {}
    
    @abstractmethod
    def extraer(self, ruta_pdf: str) -> Dict[str, Any]:
        """
        Método abstracto que debe ser implementado por cada extractor.
        """
        pass
    
    def _leer_pdf(self, ruta_pdf: str) -> Optional[str]:
        """
        Lee el PDF y devuelve el texto completo.
        
        Args:
            ruta_pdf (str): Ruta al archivo PDF
            
        Returns:
            str: Texto completo del PDF o None si hay error
        """
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                texto_completo = ""
                for pagina in pdf.pages:
                    texto_completo += pagina.extract_text() or ""
                self.texto = texto_completo
                return texto_completo
        except Exception as e:
            print(f"❌ Error al leer PDF: {e}")
            return None
    
    def _buscar_patron(self, patron: str, grupo: int = 1) -> Optional[str]:
        """
        Busca un patrón en el texto y devuelve el grupo especificado.
        
        Args:
            patron (str): Patrón Regex
            grupo (int): Número del grupo a devolver
            
        Returns:
            str: Valor encontrado o None
        """
        if not self.texto:
            return None
        match = re.search(patron, self.texto, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(grupo).strip()
        return None
    
    def _buscar_todos_patrones(self, patron: str, grupo: int = 1) -> List[str]:
        """
        Busca todas las coincidencias de un patrón.
        
        Args:
            patron (str): Patrón Regex
            grupo (int): Número del grupo a devolver
            
        Returns:
            list: Lista de valores encontrados
        """
        if not self.texto:
            return []
        matches = re.findall(patron, self.texto, re.IGNORECASE | re.MULTILINE)
        if matches:
            if isinstance(matches[0], tuple):
                return [m[grupo-1].strip() for m in matches if len(m) >= grupo]
            return [m.strip() for m in matches]
        return []
    
    def _limpiar_monto(self, valor_str: str) -> float:
        """
        Convierte texto de monto a número float.
        
        Args:
            valor_str (str): Texto del monto
            
        Returns:
            float: Valor numérico del monto
        """
        if not valor_str:
            return 0.0
        
        # Eliminar todo excepto números, punto y coma
        valor_limpio = re.sub(r'[^\d.,]', '', valor_str)
        # Reemplazar coma por punto (para decimales)
        valor_limpio = valor_limpio.replace(',', '.')
        
        try:
            return float(valor_limpio)
        except ValueError:
            return 0.0
    
    def _extraer_fecha(self, patron: str) -> Optional[datetime]:
        """
        Extrae y convierte una fecha.
        
        Args:
            patron (str): Patrón Regex para la fecha
            
        Returns:
            datetime: Objeto datetime o None si no se encuentra
        """
        fecha_str = self._buscar_patron(patron)
        if not fecha_str:
            return None
        
        # Intentar diferentes formatos
        for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d.%m.%Y']:
            try:
                return datetime.strptime(fecha_str, fmt)
            except ValueError:
                continue
        return None
    
    def _extraer_productos(self, patron: str) -> List[Dict]:
        """
        Extrae productos de una lista usando un patrón.
        
        Args:
            patron (str): Patrón Regex para productos
            
        Returns:
            list: Lista de diccionarios con los productos
        """
        if not self.texto:
            return []
        
        productos = []
        matches = re.findall(patron, self.texto, re.IGNORECASE)
        
        for match in matches:
            if isinstance(match, tuple):
                if len(match) >= 3:
                    producto = {}
                    try:
                        producto['cantidad'] = self._limpiar_monto(match[0])
                    except:
                        producto['cantidad'] = 1
                    
                    producto['descripcion'] = match[1].strip() if len(match) > 1 else ""
                    
                    if len(match) > 2:
                        producto['precio_unitario'] = self._limpiar_monto(match[2])
                    if len(match) > 3:
                        producto['total'] = self._limpiar_monto(match[3])
                    
                    productos.append(producto)
            else:
                productos.append({'descripcion': match.strip()})
        
        return productos
    
    def _extraer_ruc(self) -> Optional[str]:
        """
        Extrae RUC del texto.
        
        Returns:
            str: RUC encontrado o None
        """
        # Buscar en diferentes formatos
        patrones = [
            r'RUC\s*[:.]?\s*(\d{11})',
            r'R\.U\.C\s*[:.]?\s*(\d{11})',
            r'(\d{11})'
        ]
        
        for patron in patrones:
            ruc = self._buscar_patron(patron)
            if ruc:
                return ruc
        return None
    
    def _extraer_telefono(self) -> Optional[str]:
        """
        Extrae teléfono del texto.
        
        Returns:
            str: Teléfono encontrado o None
        """
        return self._buscar_patron(r'(?:TELÉFONO|TEL|TELEFONO)\s*[:.]?\s*([\d\s\-\(\)]+)')
    
    def _extraer_direccion(self) -> Optional[str]:
        """
        Extrae dirección del texto.
        
        Returns:
            str: Dirección encontrada o None
        """
        return self._buscar_patron(r'(?:DIRECCIÓN|DIRECCION|DOMICILIO)\s*[:.]?\s*([^\n]{10,})')
    
    def _limpiar_texto(self, texto: str) -> str:
        """
        Limpia el texto eliminando espacios extras y caracteres especiales.
        
        Args:
            texto (str): Texto a limpiar
            
        Returns:
            str: Texto limpio
        """
        if not texto:
            return ""
        # Eliminar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        # Eliminar espacios al inicio y final
        return texto.strip()