# src/utils/backup_manager.py
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class BackupManager:
    """Gestor de copias de seguridad"""
    
    def __init__(self, db_path: str = None):
        self.base_dir = Path(__file__).parent.parent.parent
        self.db_path = db_path or str(self.base_dir / 'contable.db')
        self.backup_dir = self.base_dir / 'data' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def crear_backup(self) -> Dict[str, Any]:
        """Crea una copia de seguridad de la base de datos"""
        try:
            # Generar nombre del backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.db"
            backup_path = self.backup_dir / backup_name
            
            # Copiar archivo
            shutil.copy2(self.db_path, backup_path)
            
            # Obtener tamaño
            size_bytes = backup_path.stat().st_size
            size_mb = round(size_bytes / (1024 * 1024), 2)
            
            return {
                'exito': True,
                'nombre': backup_name,
                'ruta': str(backup_path),
                'fecha': datetime.now().isoformat(),
                'tamaño': size_mb,  # ← AHORA ES NUMÉRICO
                'tamaño_str': f"{size_mb} MB"
            }
        except Exception as e:
            return {'exito': False, 'error': str(e)}
    
    def listar_backups(self) -> List[Dict[str, Any]]:
        """Lista todos los backups disponibles"""
        backups = []
        for archivo in self.backup_dir.glob('backup_*.db'):
            stats = archivo.stat()
            size_mb = round(stats.st_size / (1024 * 1024), 2)
            backups.append({
                'nombre': archivo.name,
                'ruta': str(archivo),
                'fecha': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                'fecha_legible': datetime.fromtimestamp(stats.st_mtime).strftime('%d/%m/%Y %H:%M'),
                'tamaño': size_mb,  # ← AHORA ES NUMÉRICO
                'tamaño_str': f"{size_mb} MB"
            })
        # Ordenar por fecha (más reciente primero)
        return sorted(backups, key=lambda x: x['fecha'], reverse=True)
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas de los backups"""
        backups = self.listar_backups()
        
        if not backups:
            return {
                'total_backups': 0,
                'total_size': 0,
                'ultimo_backup': None,
                'backups_por_mes': {}
            }
        
        # Calcular tamaño total (seguro)
        total_size = 0
        for b in backups:
            total_size += b.get('tamaño', 0)
        
        # Agrupar por mes
        meses = {}
        for b in backups:
            fecha_str = b.get('fecha', '')
            if fecha_str:
                try:
                    fecha = datetime.fromisoformat(fecha_str)
                    mes_key = fecha.strftime('%Y-%m')
                    meses[mes_key] = meses.get(mes_key, 0) + 1
                except:
                    pass
        
        return {
            'total_backups': len(backups),
            'total_size': round(total_size, 2),
            'ultimo_backup': backups[0] if backups else None,
            'backups_por_mes': meses
        }
    
    def restaurar_backup(self, nombre_backup: str) -> bool:
        """Restaura un backup específico"""
        backup_path = self.backup_dir / nombre_backup
        if not backup_path.exists():
            return False
        
        try:
            # Hacer backup del archivo actual antes de restaurar
            if os.path.exists(self.db_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                shutil.copy2(self.db_path, f"{self.db_path}.{timestamp}.bak")
            
            # Restaurar
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            print(f"Error al restaurar: {e}")
            return False