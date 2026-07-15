# src/extractors/base.py
# ======================
# Clase base para extractores

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExtractor(ABC):
    """Clase base para todos los extractores."""
    
    @abstractmethod
    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extrae datos del texto del PDF.
        
        Args:
            text: Texto extraído del PDF
            
        Returns:
            Dict: Datos estructurados
        """
        pass
    
    def _parse_monto(self, value: str) -> float:
        """Convierte string de monto a float."""
        try:
            import re
            cleaned = value.replace('.', '').replace(',', '.')
            cleaned = re.sub(r'[^\d.]', '', cleaned)
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0.0
