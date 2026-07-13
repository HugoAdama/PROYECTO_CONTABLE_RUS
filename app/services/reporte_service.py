# app/services/reporte_service.py
from sqlalchemy import func
from app import db
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion
from src.calculators.calculadora_rus import CalculadoraRUS


class ReporteService:
    """Servicio para generar datos de reportes y gráficos"""

    @staticmethod
    def get_ventas_mensuales(mes=None, anio=None):
        query = db.session.query(
            BoletaVenta.anio,
            BoletaVenta.mes,
            func.sum(BoletaVenta.monto).label('total')
        ).group_by(BoletaVenta.anio, BoletaVenta.mes)

        if mes and anio:
            query = query.filter(BoletaVenta.mes == mes, BoletaVenta.anio == anio)
        elif anio:
            query = query.filter(BoletaVenta.anio == anio)

        resultados = query.order_by(BoletaVenta.anio, BoletaVenta.mes).all()

        meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                         'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        datos = {f"{r.anio}-{r.mes:02d}": r.total for r in resultados}
        fechas_ordenadas = sorted(datos.keys())
        meses = [f"{meses_nombres[int(f.split('-')[1])-1]} {f.split('-')[0]}" for f in fechas_ordenadas]
        montos = [datos[f] for f in fechas_ordenadas]

        return {
            'meses': meses,
            'montos': montos,
            'total_general': sum(montos),
            'promedio': sum(montos) / len(montos) if montos else 0
        }

    @staticmethod
    def get_compras_mensuales(mes=None, anio=None):
        query = db.session.query(
            FacturaCompra.anio,
            FacturaCompra.mes,
            func.sum(FacturaCompra.monto).label('total')
        ).group_by(FacturaCompra.anio, FacturaCompra.mes)

        if mes and anio:
            query = query.filter(FacturaCompra.mes == mes, FacturaCompra.anio == anio)
        elif anio:
            query = query.filter(FacturaCompra.anio == anio)

        resultados = query.order_by(FacturaCompra.anio, FacturaCompra.mes).all()

        meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                         'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        datos = {f"{r.anio}-{r.mes:02d}": r.total for r in resultados}
        fechas_ordenadas = sorted(datos.keys())
        meses = [f"{meses_nombres[int(f.split('-')[1])-1]} {f.split('-')[0]}" for f in fechas_ordenadas]
        montos = [datos[f] for f in fechas_ordenadas]

        return {
            'meses': meses,
            'montos': montos,
            'total_general': sum(montos),
            'promedio': sum(montos) / len(montos) if montos else 0
        }

    @staticmethod
    def get_evolucion_impuestos(mes=None, anio=None):
        ventas_data = ReporteService.get_ventas_mensuales(mes, anio)

        meses = ventas_data['meses']
        impuestos = []

        for monto in ventas_data['montos']:
            if monto <= 5000:
                impuesto = 20
            elif monto <= 8000:
                impuesto = 50
            else:
                impuesto = monto * 0.05
            impuestos.append(impuesto)

        return {
            'meses': meses,
            'impuestos': impuestos,
            'total_impuestos': sum(impuestos),
            'promedio_impuestos': sum(impuestos) / len(impuestos) if impuestos else 0
        }

    @staticmethod
    def get_distribucion_gastos(mes=None, anio=None):
        query = db.session.query(
            FacturaCompra.proveedor,
            func.sum(FacturaCompra.monto).label('total')
        ).filter(
            FacturaCompra.proveedor.isnot(None),
            FacturaCompra.proveedor != ''
        )

        if mes and anio:
            query = query.filter(FacturaCompra.mes == mes, FacturaCompra.anio == anio)
        elif anio:
            query = query.filter(FacturaCompra.anio == anio)

        resultados = query.group_by(FacturaCompra.proveedor).order_by(
            func.sum(FacturaCompra.monto).desc()
        ).all()

        proveedores = []
        montos = []

        for i, r in enumerate(resultados):
            if i < 5:
                nombre = r.proveedor[:20] + '...' if len(r.proveedor) > 20 else r.proveedor
                proveedores.append(nombre)
                montos.append(r.total)
            else:
                if len(proveedores) >= 5 and len(resultados) > 5:
                    if proveedores[-1] == 'Otros':
                        montos[-1] += r.total
                    else:
                        proveedores.append('Otros')
                        montos.append(r.total)
                break

        return {
            'proveedores': proveedores,
            'montos': montos,
            'total_gastos': sum(montos)
        }

    @staticmethod
    def get_resumen_general():
        total_ventas = db.session.query(func.sum(BoletaVenta.monto)).scalar() or 0
        total_compras = db.session.query(func.sum(FacturaCompra.monto)).scalar() or 0
        total_percepciones = db.session.query(func.sum(Percepcion.monto)).scalar() or 0

        ultimo_mes = db.session.query(
            BoletaVenta.anio, BoletaVenta.mes
        ).order_by(BoletaVenta.anio.desc(), BoletaVenta.mes.desc()).first()

        ventas_ultimo_mes = 0
        if ultimo_mes:
            ventas_ultimo_mes = db.session.query(
                func.sum(BoletaVenta.monto)
            ).filter(
                BoletaVenta.anio == ultimo_mes[0],
                BoletaVenta.mes == ultimo_mes[1]
            ).scalar() or 0

        # ✅ CORREGIDO: usar calcular_estado (no calcular_estado_rus)
        estado, impuesto = CalculadoraRUS.calcular_estado(ventas_ultimo_mes)

        num_facturas = FacturaCompra.query.count()
        num_boletas = BoletaVenta.query.count()
        num_percepciones = Percepcion.query.count()

        return {
            'total_ventas': total_ventas,
            'total_compras': total_compras,
            'total_percepciones': total_percepciones,
            'ventas_ultimo_mes': ventas_ultimo_mes,
            'estado_rus': estado,
            'impuesto_mensual': impuesto,
            'num_facturas': num_facturas,
            'num_boletas': num_boletas,
            'num_percepciones': num_percepciones,
            'ultimo_mes': f"{ultimo_mes[1]:02d}/{ultimo_mes[0]}" if ultimo_mes else 'Sin datos'
        }

    @staticmethod
    def get_datos_completos_reportes(mes=None, anio=None):
        return {
            'ventas': ReporteService.get_ventas_mensuales(mes, anio),
            'compras': ReporteService.get_compras_mensuales(mes, anio),
            'impuestos': ReporteService.get_evolucion_impuestos(mes, anio),
            'distribucion': ReporteService.get_distribucion_gastos(mes, anio),
            'resumen': ReporteService.get_resumen_general()
        }

    @staticmethod
    def get_años_disponibles():
        años = db.session.query(BoletaVenta.anio).distinct().order_by(BoletaVenta.anio.desc()).all()
        años_facturas = db.session.query(FacturaCompra.anio).distinct().order_by(FacturaCompra.anio.desc()).all()

        todos_años = set()
        for a in años:
            if a[0] is not None:
                todos_años.add(a[0])
        for a in años_facturas:
            if a[0] is not None:
                todos_años.add(a[0])

        return sorted(list(todos_años), reverse=True)

    @staticmethod
    def get_meses_disponibles(anio):
        if not anio:
            return []

        meses = db.session.query(BoletaVenta.mes).filter(BoletaVenta.anio == anio).distinct().order_by(BoletaVenta.mes).all()
        meses_facturas = db.session.query(FacturaCompra.mes).filter(FacturaCompra.anio == anio).distinct().order_by(FacturaCompra.mes).all()

        todos_meses = set()
        for m in meses:
            if m[0] is not None:
                todos_meses.add(m[0])
        for m in meses_facturas:
            if m[0] is not None:
                todos_meses.add(m[0])

        return sorted(list(todos_meses))