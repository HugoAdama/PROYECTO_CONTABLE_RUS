# app/services/reporte_service.py
from app import db
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion
from src.calculators.calculadora_rus import CalculadoraRUS
from sqlalchemy import func
from datetime import datetime

class ReporteService:
    
    @staticmethod
    def get_datos_completos_reportes(mes=None, anio=None):
        """Obtiene datos completos para reportes con gráficos"""
        
        # ============================================
        # OBTENER TODOS LOS DATOS
        # ============================================
        facturas = FacturaCompra.query.all()
        boletas = BoletaVenta.query.all()
        percepciones = Percepcion.query.all()
        
        # ============================================
        # APLICAR FILTROS
        # ============================================
        if mes and anio:
            facturas = [f for f in facturas if f.mes == mes and f.anio == anio]
            boletas = [b for b in boletas if b.mes == mes and b.anio == anio]
            percepciones = [p for p in percepciones if p.mes == mes and p.anio == anio]
        elif anio:
            facturas = [f for f in facturas if f.anio == anio]
            boletas = [b for b in boletas if b.anio == anio]
            percepciones = [p for p in percepciones if p.anio == anio]
        elif mes:
            facturas = [f for f in facturas if f.mes == mes]
            boletas = [b for b in boletas if b.mes == mes]
            percepciones = [p for p in percepciones if p.mes == mes]
        
        # ============================================
        # CALCULAR TOTALES
        # ============================================
        total_ventas = sum(b.monto for b in boletas) if boletas else 0
        total_compras = sum(f.monto for f in facturas) if facturas else 0
        total_percepciones = sum(p.monto for p in percepciones) if percepciones else 0
        
        # ============================================
        # CALCULAR ESTADO RUS
        # ============================================
        # Ventas del mes actual (si hay filtro)
        ventas_mes = total_ventas
        
        # Si no hay filtro, usar el último mes con datos
        if not mes and not anio and boletas:
            ultima_boleta = max(boletas, key=lambda x: x.fecha_emision)
            ventas_mes = sum(b.monto for b in boletas if b.mes == ultima_boleta.mes and b.anio == ultima_boleta.anio)
        
        estado, impuesto = CalculadoraRUS.calcular_estado(ventas_mes)
        
        # ============================================
        # DATOS PARA GRÁFICOS
        # ============================================
        # Ventas por mes
        ventas_por_mes = {}
        for b in boletas:
            key = f"{b.anio}-{b.mes:02d}"
            ventas_por_mes[key] = ventas_por_mes.get(key, 0) + b.monto
        
        # Compras por mes
        compras_por_mes = {}
        for f in facturas:
            key = f"{f.anio}-{f.mes:02d}"
            compras_por_mes[key] = compras_por_mes.get(key, 0) + f.monto
        
        # Impuestos por mes (simulado)
        impuestos_por_mes = {}
        for key in ventas_por_mes:
            _, impuesto_mes = CalculadoraRUS.calcular_estado(ventas_por_mes[key])
            impuestos_por_mes[key] = impuesto_mes
        
        # Distribución por proveedor
        distribucion = {}
        for f in facturas:
            proveedor = f.proveedor or 'Otros'
            distribucion[proveedor] = distribucion.get(proveedor, 0) + f.monto
        
        # ============================================
        # RETORNAR ESTRUCTURA COMPLETA
        # ============================================
        return {
            'total_ventas': total_ventas,
            'total_compras': total_compras,
            'total_percepciones': total_percepciones,
            'estado_rus': estado,
            'impuesto_mensual': impuesto,
            'ventas_por_mes': ventas_por_mes,
            'compras_por_mes': compras_por_mes,
            'impuestos_por_mes': impuestos_por_mes,
            'distribucion': distribucion,
            'total_facturas': len(facturas),
            'total_boletas': len(boletas),
            'total_percepciones_count': len(percepciones),
            'total_documentos': len(facturas) + len(boletas) + len(percepciones),
            'ultimo_mes': f"{datetime.now().month:02d}/{datetime.now().year}" if boletas else None
        }