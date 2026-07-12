"""
Script para limpiar documentos duplicados en la base de datos
"""
import sqlite3
from pathlib import Path

# Obtener la ruta de la base de datos (en la raíz del proyecto)
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / 'contable.db'

print(f"📁 Ruta de la base de datos: {DB_PATH}")
print("=" * 50)

if not DB_PATH.exists():
    print(f"❌ Error: No se encuentra la base de datos en {DB_PATH}")
    exit(1)

conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

print("🗑️ LIMPIANDO DUPLICADOS")
print("=" * 50)

try:
    # Verificar cuántas facturas con 'DESCONOCIDO' existen
    cursor.execute("SELECT COUNT(*) FROM facturas_compras WHERE numero_factura = 'DESCONOCIDO'")
    count_desconocido = cursor.fetchone()[0]
    print(f"📄 Facturas con 'DESCONOCIDO': {count_desconocido}")

    if count_desconocido > 0:
        confirmar = input(f"¿Eliminar {count_desconocido} facturas con número 'DESCONOCIDO'? (s/n): ")
        if confirmar.lower() == 's':
            cursor.execute("DELETE FROM facturas_compras WHERE numero_factura = 'DESCONOCIDO'")
            print(f"✅ Eliminadas {cursor.rowcount} facturas")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error en facturas: {e}")

try:
    # Verificar facturas con '20101796' (número inválido)
    cursor.execute("SELECT COUNT(*) FROM facturas_compras WHERE numero_factura = '20101796'")
    count_invalido = cursor.fetchone()[0]
    print(f"📄 Facturas con '20101796': {count_invalido}")

    if count_invalido > 0:
        confirmar = input(f"¿Eliminar {count_invalido} facturas con número '20101796'? (s/n): ")
        if confirmar.lower() == 's':
            cursor.execute("DELETE FROM facturas_compras WHERE numero_factura = '20101796'")
            print(f"✅ Eliminadas {cursor.rowcount} facturas")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error en facturas: {e}")

conn.commit()
conn.close()
print("✅ Limpieza completada")