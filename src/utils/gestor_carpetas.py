# src/utils/gestor_carpetas.py
"""
📁 GESTOR DE CARPETAS AUTOMÁTICO
Crea y organiza carpetas por mes y año automáticamente
"""

from pathlib import Path
import os
from datetime import datetime

class GestorCarpetas:
    """Gestor de carpetas para organizar PDFs por mes y año"""
    
    def __init__(self, base_path="data/pdfs"):
        self.base_path = Path(base_path)
        self.tipos = ["facturas", "boletas", "percepciones"]
        self._crear_estructura_base()
    
    def _crear_estructura_base(self):
        """Crea la estructura base de carpetas si no existe"""
        for tipo in self.tipos:
            carpeta = self.base_path / tipo
            carpeta.mkdir(parents=True, exist_ok=True)
    
    def obtener_carpeta_mes(self, tipo, mes, año):
        """
        Obtiene la ruta de la carpeta para un mes específico.
        Si no existe, la crea automáticamente.
        """
        if tipo not in self.tipos:
            raise ValueError(f"Tipo inválido: {tipo}. Debe ser: {', '.join(self.tipos)}")
        
        mes_str = f"{año}_{mes:02d}"
        carpeta = self.base_path / tipo / mes_str
        carpeta.mkdir(parents=True, exist_ok=True)
        return carpeta
    
    def obtener_todos_meses(self, tipo):
        """Obtiene todas las carpetas de meses para un tipo"""
        if tipo not in self.tipos:
            raise ValueError(f"Tipo inválido: {tipo}")
        
        carpeta_tipo = self.base_path / tipo
        if not carpeta_tipo.exists():
            return []
        
        meses = []
        for carpeta in carpeta_tipo.iterdir():
            if carpeta.is_dir():
                try:
                    # Formato: año_mes (ej: 2026_04)
                    nombre = carpeta.name
                    año, mes = nombre.split('_')
                    meses.append({
                        'ruta': carpeta,
                        'nombre': nombre,
                        'año': int(año),
                        'mes': int(mes),
                        'documentos': len(list(carpeta.glob("*.pdf")))
                    })
                except ValueError:
                    continue
        
        return sorted(meses, key=lambda x: x['nombre'], reverse=True)
    
    def contar_documentos(self, tipo, mes=None, año=None):
        """Cuenta los documentos en una carpeta"""
        if mes and año:
            carpeta = self.obtener_carpeta_mes(tipo, mes, año)
            return len(list(carpeta.glob("*.pdf")))
        else:
            total = 0
            carpeta_tipo = self.base_path / tipo
            if carpeta_tipo.exists():
                for mes_carpeta in carpeta_tipo.iterdir():
                    if mes_carpeta.is_dir():
                        total += len(list(mes_carpeta.glob("*.pdf")))
            return total
    
    def obtener_resumen_completo(self):
        """Obtiene un resumen completo de todos los documentos"""
        resumen = {}
        for tipo in self.tipos:
            meses = self.obtener_todos_meses(tipo)
            total = sum(m['documentos'] for m in meses)
            resumen[tipo] = {
                'meses': meses,
                'total_documentos': total
            }
        return resumen