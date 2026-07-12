# src/utils/backup_manager.py
"""
💾 GESTOR DE BACKUPS
Copia de seguridad automática de la base de datos
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import streamlit as st

class BackupManager:
    """Gestor de backups automáticos"""
    
    def __init__(self):
        self.db_path = Path("contable.db")
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def crear_backup(self):
        """
        Crea una copia de seguridad de la base de datos.
        
        Returns:
            str: Ruta del backup creado
        """
        if not self.db_path.exists():
            raise FileNotFoundError("Base de datos no encontrada")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.db"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(self.db_path, backup_path)
        
        # Mantener solo los últimos 10 backups
        self._limpiar_backups_antiguos()
        
        return str(backup_path)
    
    def _limpiar_backups_antiguos(self):
        """Elimina backups antiguos (mantiene los 10 más recientes)"""
        backups = sorted(self.backup_dir.glob("backup_*.db"))
        if len(backups) > 10:
            for backup in backups[:-10]:
                backup.unlink()
    
    def listar_backups(self):
        """
        Lista todos los backups disponibles.
        
        Returns:
            list: Lista de backups con su información
        """
        backups = []
        for backup in sorted(self.backup_dir.glob("backup_*.db"), reverse=True):
            size = backup.stat().st_size / 1024  # KB
            date_str = backup.stem.replace("backup_", "")
            backups.append({
                'nombre': backup.name,
                'ruta': str(backup),
                'fecha': date_str,
                'tamaño': f"{size:.1f} KB"
            })
        return backups
    
    def restaurar_backup(self, nombre_backup):
        """
        Restaura un backup específico.
        
        Args:
            nombre_backup (str): Nombre del archivo de backup
        
        Returns:
            bool: True si se restauró correctamente
        """
        backup_path = self.backup_dir / nombre_backup
        
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup no encontrado: {nombre_backup}")
        
        # Crear backup del estado actual antes de restaurar
        self.crear_backup()
        
        # Restaurar backup
        shutil.copy2(backup_path, self.db_path)
        
        return True
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas de los backups.
        
        Returns:
            dict: Estadísticas de backups
        """
        backups = self.listar_backups()
        total_size = sum(b['tamaño'] for b in backups)
        
        return {
            'total_backups': len(backups),
            'tamaño_total': total_size,
            'ultimo_backup': backups[0]['fecha'] if backups else None
        }