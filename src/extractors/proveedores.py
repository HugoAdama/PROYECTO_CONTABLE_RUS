# src/extractors/proveedores.py
"""
🏪 DETECCIÓN DE PROVEEDORES
Identifica el proveedor de una factura automáticamente
"""

import re

class ProveedorDetector:
    """Detecta el proveedor de una factura basado en el texto."""
    
    # Patrones de identificación por proveedor
    PATRONES = {
        'natura': [
            r'NATURA COSMÉTICOS',
            r'Natura Cosméticos',
            r'R\.U\.C:\s*20101796532',
        ],
        'avon': [
            r'AVON COSMÉTICOS',
            r'Avon Cosmetics',
            r'R\.U\.C:\s*20100015708',
        ],
        'ebel': [
            r'EBEL COSMÉTICOS',
            r'Ebel Cosméticos',
            r'R\.U\.C:\s*20100016963',
        ],
        'yanbal': [
            r'YANBAL COSMÉTICOS',
            r'Yanbal Cosméticos',
            r'R\.U\.C:\s*20100013072',
        ],
        'esika': [
            r'ESIKA COSMÉTICOS',
            r'Esika Cosméticos',
            r'R\.U\.C:\s*20100013900',
        ],
        'lbel': [
            r'LBEL COSMÉTICOS',
            r'Lbel Cosméticos',
            r'R\.U\.C:\s*20100015555',
        ],
        'cyzone': [
            r'CYZONE COSMÉTICOS',
            r'Cyzone Cosméticos',
            r'R\.U\.C:\s*20100016666',
        ],
    }
    
    @classmethod
    def detectar(cls, texto: str) -> str:
        """
        Detecta el proveedor a partir del texto.
        
        Returns:
            str: Nombre del proveedor ('natura', 'avon', 'ebel', etc.)
        """
        texto = texto.upper()
        
        for proveedor, patrones in cls.PATRONES.items():
            for patron in patrones:
                if re.search(patron, texto, re.IGNORECASE):
                    return proveedor
        
        return 'desconocido'
    
    @classmethod
    def obtener_ruc(cls, proveedor: str) -> str:
        """Obtiene el RUC de un proveedor."""
        rucs = {
            'natura': '20101796532',
            'avon': '20100015708',
            'ebel': '20100016963',
            'yanbal': '20100013072',
            'esika': '20100013900',
            'lbel': '20100015555',
            'cyzone': '20100016666',
        }
        return rucs.get(proveedor, '')
    
    @classmethod
    def obtener_nombre(cls, proveedor: str) -> str:
        """Obtiene el nombre completo de un proveedor."""
        nombres = {
            'natura': 'Natura Cosméticos S.A.',
            'avon': 'Avon Cosméticos S.A.',
            'ebel': 'Ebel Cosméticos S.A.',
            'yanbal': 'Yanbal Cosméticos S.A.',
            'esika': 'Esika Cosméticos S.A.',
            'lbel': 'Lbel Cosméticos S.A.',
            'cyzone': 'Cyzone Cosméticos S.A.',
        }
        return nombres.get(proveedor, 'Proveedor Desconocido')