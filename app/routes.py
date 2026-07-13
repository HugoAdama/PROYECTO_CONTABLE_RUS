from flask import Blueprint, render_template, request, jsonify, send_file
from app.services.reporte_service import ReporteService
from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository
from src.calculators.calculadora_rus import CalculadoraRUS
from datetime import datetime

main_bp = Blueprint('main', __name__)

factura_repo = FacturaRepository()
boleta_repo = BoletaRepository()
percepcion_repo = PercepcionRepository()


@main_bp.route('/')
def index():
    facturas = factura_repo.get_all()
    boletas = boleta_repo.get_all()
    percepciones = percepcion_repo.get_all()
    
    total_ventas = sum(b.monto for b in boletas) if boletas else 0
    total_compras = sum(f.monto for f in facturas) if facturas else 0
    total_percepciones = sum(p.monto for p in percepciones) if percepciones else 0
    
    ultimo_mes = None
    if boletas:
        ultima_boleta = max(boletas, key=lambda x: x.fecha_emision)
        ultimo_mes = {
            'mes': ultima_boleta.mes,
            'anio': ultima_boleta.anio,
            'nombre_mes': ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][ultima_boleta.mes-1]
        }
    
    ventas_ultimo_mes = 0
    if ultimo_mes:
        ventas_ultimo_mes = sum(b.monto for b in boletas if b.mes == ultimo_mes['mes'] and b.anio == ultimo_mes['anio'])
    
    estado, impuesto = CalculadoraRUS.calcular_estado(ventas_ultimo_mes)
    
    utilidad = total_ventas - total_compras
    porcentaje_utilidad = (utilidad / total_ventas * 100) if total_ventas > 0 else 0
    
    return render_template('index.html',
                         total_ventas=total_ventas,
                         total_compras=total_compras,
                         total_percepciones=total_percepciones,
                         total_boletas=len(boletas),
                         total_facturas=len(facturas),
                         total_percepciones_count=len(percepciones),
                         estado_rus=estado,
                         impuesto_mensual=impuesto,
                         ultimo_mes=ultimo_mes,
                         utilidad=utilidad,
                         porcentaje_utilidad=porcentaje_utilidad,
                         variacion_ventas=12,
                         variacion_compras=-8,
                         total_documentos=len(facturas) + len(boletas) + len(percepciones),
                         facturas=facturas[:5],
                         boletas=boletas[:5])


@main_bp.route('/subir')
def subir():
    return render_template('subir.html')


@main_bp.route('/ver_datos')
def ver_datos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    tipo = request.args.get('tipo', 'todos')
    
    facturas = factura_repo.get_all()
    boletas = boleta_repo.get_all()
    percepciones = percepcion_repo.get_all()
    
    if mes and anio:
        facturas = [f for f in facturas if f.mes == mes and f.anio == anio]
        boletas = [b for b in boletas if b.mes == mes and b.anio == anio]
        percepciones = [p for p in percepciones if p.mes == mes and p.anio == anio]
    
    todos_items = []
    if tipo in ['todos', 'facturas']:
        for f in facturas:
            todos_items.append({
                'tipo': 'Factura',
                'id': f.id,
                'numero': f.numero,
                'fecha': f.fecha_emision,
                'monto': f.monto,
                'proveedor_cliente': f.proveedor,
                'descripcion': f.descripcion,
                'archivo': f.archivo
            })
    if tipo in ['todos', 'boletas']:
        for b in boletas:
            todos_items.append({
                'tipo': 'Boleta',
                'id': b.id,
                'numero': b.numero,
                'fecha': b.fecha_emision,
                'monto': b.monto,
                'proveedor_cliente': b.cliente,
                'descripcion': b.descripcion,
                'archivo': b.archivo
            })
    if tipo in ['todos', 'percepciones']:
        for p in percepciones:
            todos_items.append({
                'tipo': 'Percepción',
                'id': p.id,
                'numero': p.numero,
                'fecha': p.fecha_emision,
                'monto': p.monto,
                'proveedor_cliente': p.proveedor,
                'descripcion': p.descripcion,
                'archivo': p.archivo
            })
    
    todos_items.sort(key=lambda x: x['fecha'], reverse=True)
    
    total_items = len(todos_items)
    total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 1
    start = (page - 1) * per_page
    end = start + per_page
    items_paginated = todos_items[start:end]
    
    años_disponibles = sorted(set([f.anio for f in facturas] + [b.anio for b in boletas] + [p.anio for p in percepciones]), reverse=True)
    
    return render_template('ver_datos.html',
                         items=items_paginated,
                         page=page,
                         per_page=per_page,
                         total_items=total_items,
                         total_pages=total_pages,
                         tipo_actual=tipo,
                         mes_actual=mes,
                         anio_actual=anio,
                         años_disponibles=años_disponibles,
                         total_registros=total_items)


@main_bp.route('/reportes')
def reportes():
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    
    datos = ReporteService.get_datos_completos_reportes(mes, anio)
    años_disponibles = ReporteService.get_años_disponibles()
    meses_disponibles = ReporteService.get_meses_disponibles(anio) if anio else []
    
    return render_template('reportes.html',
                         datos=datos,
                         mes_actual=mes,
                         anio_actual=anio,
                         años_disponibles=años_disponibles,
                         meses_disponibles=meses_disponibles)


@main_bp.route('/api/reportes/datos')
def api_reportes_datos():
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    
    datos = ReporteService.get_datos_completos_reportes(mes, anio)
    return jsonify(datos)


@main_bp.route('/carpetas')
def carpetas():
    return render_template('carpetas.html')


@main_bp.route('/backup')
def backup():
    return render_template('backup.html')


@main_bp.route('/historial')
def historial():
    return render_template('historial.html')


@main_bp.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')


@main_bp.route('/exportar/excel')
def exportar_excel():
    try:
        from app.services.export_service import ExportService
        
        mes = request.args.get('mes', type=int)
        anio = request.args.get('anio', type=int)
        
        excel_data = ExportService.exportar_reporte_completo(mes, anio)
        
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'reporte_RUS_{fecha_actual}.xlsx'
        
        return send_file(
            excel_data,
            download_name=nombre_archivo,
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except ImportError:
        return jsonify({'error': 'Servicio de exportación no disponible'}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500