"""
Script para migrar archivos PDF antiguos a la nueva estructura de carpetas
"""
import os
import shutil
from pathlib import Path
import re

# Obtener la ruta del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT / 'data'

def identificar_tipo_y_fecha(nombre_archivo):
    """Identifica el tipo y fecha de un archivo PDF por su nombre"""
    nombre = nombre_archivo.lower()
    
    # Identificar tipo
    if 'boleta' in nombre or 'eb' in nombre:
        tipo = 'boletas'
    elif 'factura' in nombre or 'f0' in nombre or 'f033' in nombre:
        tipo = 'facturas'
    elif 'percepcion' in nombre or 'p0' in nombre:
        tipo = 'percepciones'
    else:
        tipo = 'pdfs'  # Carpeta por defecto
    
    # Intentar extraer fecha del nombre (YYYYMMDD)
    fecha_match = re.search(r'(\d{4})(\d{2})(\d{2})', nombre)
    if fecha_match:
        anio = fecha_match.group(1)
        mes = fecha_match.group(2)
    else:
        # Si no hay fecha, usar 2026_05 como default
        anio = '2026'
        mes = '05'
    
    return tipo, anio, mes

def migrar_archivos():
    """Migra archivos de data/pdfs/ a la nueva estructura"""
    pdfs_folder = DATA_FOLDER / 'pdfs'
    if not pdfs_folder.exists():
        print("📁 La carpeta data/pdfs/ no existe")
        return
    
    archivos = list(pdfs_folder.glob('*.pdf'))
    if not archivos:
        print("📁 No hay archivos PDF en data/pdfs/")
        return
    
    print(f"📄 Encontrados {len(archivos)} archivos para migrar")
    
    movidos = 0
    for archivo in archivos:
        # Identificar tipo y fecha
        tipo, anio, mes = identificar_tipo_y_fecha(archivo.name)
        
        # Crear carpeta destino
        carpeta_destino = DATA_FOLDER / tipo / f"{anio}_{mes}"
        carpeta_destino.mkdir(parents=True, exist_ok=True)
        
        # Mover archivo
        destino = carpeta_destino / archivo.name
        if destino.exists():
            print(f"⚠️ {archivo.name} ya existe en {carpeta_destino}")
        else:
            shutil.move(str(archivo), str(destino))
            print(f"✅ Movido: {archivo.name} → {carpeta_destino}")
            movidos += 1
    
    # Verificar si la carpeta pdfs quedó vacía
    if not list(pdfs_folder.glob('*')):
        pdfs_folder.rmdir()
        print("🗑️ Carpeta data/pdfs/ eliminada (estaba vacía)")
    else:
        print(f"📁 La carpeta data/pdfs/ aún contiene {len(list(pdfs_folder.glob('*')))} elementos")

    print(f"\n📊 Resumen: {movidos} archivos migrados")

if __name__ == "__main__":
    print("🔄 Iniciando migración de archivos PDF...")
    print(f"📁 Carpeta de datos: {DATA_FOLDER}")
    migrar_archivos()
    print("✅ Migración completada")