# src/utils/backup_manager.py
import shutil
from pathlib import Path
from datetime import datetime
import os

class BackupManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.db_path = self.base_dir / 'contable.db'
        self.backup_dir = self.base_dir / 'data' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def crear_backup(self):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre = f"backup_{timestamp}.db"
            destino = self.backup_dir / nombre
            shutil.copy2(self.db_path, destino)
            return {'exito': True, 'nombre': nombre, 'ruta': str(destino)}
        except Exception as e:
            return {'exito': False, 'error': str(e)}

    def listar_backups(self):
        backups = []
        for archivo in sorted(self.backup_dir.glob('backup_*.db'), reverse=True):
            stats = archivo.stat()
            backups.append({
                'nombre': archivo.name,
                'fecha': datetime.fromtimestamp(stats.st_mtime).strftime('%d/%m/%Y %H:%M'),
                'tamaño': round(stats.st_size / (1024 * 1024), 2),
                'ruta': str(archivo)
            })
        return backups

    def obtener_estadisticas(self):
        backups = self.listar_backups()
        total_size = sum(b['tamaño'] for b in backups)
        return {
            'total_backups': len(backups),
            'total_size': round(total_size, 2),
            'ultimo_backup': backups[0] if backups else None
        }

    def restaurar_backup(self, nombre):
        origen = self.backup_dir / nombre
        if origen.exists():
            shutil.copy2(origen, self.db_path)
            return True
        return False