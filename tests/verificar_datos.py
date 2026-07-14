"""
Script para verificar los datos en la base de datos
Ejecutar desde la raíz: python verificar_datos.py
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion

app = create_app()

with app.app_context():
    print("=" * 70)
    print("📊 VERIFICANDO DATOS EN BASE DE DATOS")
    print("=" * 70)
    
    # ============================================
    # CONTAR REGISTROS
    # ============================================
    
    total_facturas = FacturaCompra.query.count()
    total_boletas = BoletaVenta.query.count()
    total_percepciones = Percepcion.query.count()
    
    print(f"\n📊 TOTAL DE REGISTROS:")
    print(f"  📄 Facturas: {total_facturas}")
    print(f"  🧾 Boletas: {total_boletas}")
    print(f"  📋 Percepciones: {total_percepciones}")
    print(f"  📦 Total: {total_facturas + total_boletas + total_percepciones}")
    
    # ============================================
    # DETALLE DE FACTURAS
    # ============================================
    
    print(f"\n📄 FACTURAS ({total_facturas}):")
    facturas = FacturaCompra.query.all()
    for f in facturas[:10]:
        mes_nombre = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][f.mes-1] if f.mes else '?'
        print(f"  - {f.numero}: S/{f.monto:.2f} | {f.fecha_emision} | Mes: {mes_nombre} ({f.mes}), Año: {f.anio}")
    
    if total_facturas > 10:
        print(f"  ... y {total_facturas - 10} más")
    
    # ============================================
    # DETALLE DE BOLETAS
    # ============================================
    
    print(f"\n🧾 BOLETAS ({total_boletas}):")
    boletas = BoletaVenta.query.all()
    for b in boletas[:10]:
        mes_nombre = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][b.mes-1] if b.mes else '?'
        print(f"  - {b.numero}: S/{b.monto:.2f} | {b.fecha_emision} | Mes: {mes_nombre} ({b.mes}), Año: {b.anio}")
    
    if total_boletas > 10:
        print(f"  ... y {total_boletas - 10} más")
    
    # ============================================
    # DETALLE DE PERCEPCIONES
    # ============================================
    
    print(f"\n📋 PERCEPCIONES ({total_percepciones}):")
    percepciones = Percepcion.query.all()
    for p in percepciones[:10]:
        mes_nombre = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][p.mes-1] if p.mes else '?'
        print(f"  - {p.numero}: S/{p.monto:.2f} | {p.fecha_emision} | Mes: {mes_nombre} ({p.mes}), Año: {p.anio}")
    
    if total_percepciones > 10:
        print(f"  ... y {total_percepciones - 10} más")
    
    # ============================================
    # AÑOS DISPONIBLES
    # ============================================
    
    años_set = set()
    for f in facturas:
        if f.anio and f.anio > 0:
            años_set.add(f.anio)
    for b in boletas:
        if b.anio and b.anio > 0:
            años_set.add(b.anio)
    for p in percepciones:
        if p.anio and p.anio > 0:
            años_set.add(p.anio)
    
    años_disponibles = sorted(list(años_set), reverse=True)
    
    print(f"\n📅 AÑOS DISPONIBLES:")
    if años_disponibles:
        for a in años_disponibles:
            print(f"  - {a}")
    else:
        print("  ❌ No hay años disponibles en los datos")
    
    # ============================================
    # MESES DISPONIBLES POR AÑO
    # ============================================
    
    print(f"\n📆 MESES DISPONIBLES POR AÑO:")
    for a in años_disponibles:
        meses_set = set()
        for f in facturas:
            if f.anio == a and f.mes and f.mes > 0:
                meses_set.add(f.mes)
        for b in boletas:
            if b.anio == a and b.mes and b.mes > 0:
                meses_set.add(b.mes)
        for p in percepciones:
            if p.anio == a and p.mes and p.mes > 0:
                meses_set.add(p.mes)
        
        meses = sorted(list(meses_set))
        nombres = [['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][m-1] for m in meses]
        print(f"  {a}: {nombres if nombres else 'Sin datos'}")
    
    # ============================================
    # RESUMEN FINANCIERO
    # ============================================
    
    total_ventas = sum(b.monto for b in boletas)
    total_compras = sum(f.monto for f in facturas)
    total_percepciones_sum = sum(p.monto for p in percepciones)
    
    print(f"\n💰 RESUMEN FINANCIERO:")
    print(f"  Total Ventas (Boletas): S/{total_ventas:.2f}")
    print(f"  Total Compras (Facturas): S/{total_compras:.2f}")
    print(f"  Total Percepciones: S/{total_percepciones_sum:.2f}")
    print(f"  Utilidad: S/{total_ventas - total_compras:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)