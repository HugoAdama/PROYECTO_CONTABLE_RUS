"""
Script para verificar los datos en la base de datos
"""
import sqlite3
import os
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

print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
print("=" * 50)

# Verificar tablas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
print(f"📋 Tablas encontradas: {[t[0] for t in tablas]}")
print("=" * 50)

try:
    # Facturas
    cursor.execute("SELECT COUNT(*) FROM facturas_compras")
    facturas_count = cursor.fetchone()[0]
    print(f"📄 Facturas: {facturas_count}")

    cursor.execute("SELECT numero_factura, proveedor, total_pagar, mes, anio FROM facturas_compras")
    facturas = cursor.fetchall()
    for f in facturas:
        print(f"  - {f[0]} | {f[1][:30] if f[1] else 'N/A'} | S/ {f[2]:.2f} | {f[3]}/{f[4]}")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error en facturas: {e}")

print("-" * 50)

try:
    # Boletas
    cursor.execute("SELECT COUNT(*) FROM boletas_venta")
    boletas_count = cursor.fetchone()[0]
    print(f"🧾 Boletas: {boletas_count}")

    cursor.execute("SELECT numero_boleta, cliente, total_pagar, mes, anio FROM boletas_venta")
    boletas = cursor.fetchall()
    for b in boletas:
        print(f"  - {b[0]} | {b[1][:30] if b[1] else 'N/A'} | S/ {b[2]:.2f} | {b[3]}/{b[4]}")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error en boletas: {e}")

print("-" * 50)

try:
    # Percepciones
    cursor.execute("SELECT COUNT(*) FROM percepciones")
    percepciones_count = cursor.fetchone()[0]
    print(f"💰 Percepciones: {percepciones_count}")

    cursor.execute("SELECT numero_comprobante, proveedor, monto, mes, anio FROM percepciones")
    percepciones = cursor.fetchall()
    for p in percepciones:
        print(f"  - {p[0]} | {p[1][:30] if p[1] else 'N/A'} | S/ {p[2]:.2f} | {p[3]}/{p[4]}")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error en percepciones: {e}")

print("=" * 50)
total = facturas_count + boletas_count + percepciones_count if 'facturas_count' in locals() and 'boletas_count' in locals() and 'percepciones_count' in locals() else 0
print(f"📊 Total de documentos: {total}")

conn.close()