# src/utils/gestor_carpetas.py
import os
from pathlib import Path
from datetime import datetime

class GestorCarpetas:
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / 'data'
    PDFS_DIR = DATA_DIR / 'pdfs'
    TIPOS = ['facturas', 'boletas', 'percepciones']

    def __init__(self):
        self._crear_estructura_base()

    def _crear_estructura_base(self):
        self.DATA_DIR.mkdir(exist_ok=True)
        self.PDFS_DIR.mkdir(exist_ok=True)
        for tipo in self.TIPOS:
            (self.PDFS_DIR / tipo).mkdir(exist_ok=True)

    def obtener_ruta_mes(self, tipo: str, mes: int, anio: int) -> Path:
        return self.PDFS_DIR / tipo / f"{anio}_{mes:02d}"

    def crear_carpeta_mes(self, tipo: str, mes: int, anio: int) -> Path:
        ruta = self.obtener_ruta_mes(tipo, mes, anio)
        ruta.mkdir(parents=True, exist_ok=True)
        return ruta

    def obtener_estadisticas(self) -> dict:
        stats = {}
        for tipo in self.TIPOS:
            ruta = self.PDFS_DIR / tipo
            stats[tipo] = {
                'total_documentos': 0,
                'carpetas': len([d for d in ruta.iterdir() if d.is_dir()]) if ruta.exists() else 0,
                'espacio_mb': 0
            }
            if ruta.exists():
                for archivo in ruta.rglob('*.pdf'):
                    stats[tipo]['total_documentos'] += 1
                    stats[tipo]['espacio_mb'] += archivo.stat().st_size / (1024 * 1024)
                stats[tipo]['espacio_mb'] = round(stats[tipo]['espacio_mb'], 2)
        return stats