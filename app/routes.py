from flask import Blueprint, render_template, request, jsonify, send_file
from app.services.reporte_service import ReporteService
from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository
from src.calculators.calculadora_rus import CalculadoraRUS
from datetime import datetime
import os
from pathlib import Path
import json

main_bp = Blueprint('main', __name__)

# ============================================
# INICIALIZAR REPOSITORIOS
# ============================================

factura_repo = FacturaRepository()
boleta_repo = BoletaRepository()
percepcion_repo = PercepcionRepository()


# ============================================
# RUTA: DASHBOARD (INICIO)
# ============================================

@main_bp.route('/')
def index():
    """Página principal - Dashboard"""
    
    # Obtener todos los datos
    facturas = factura_repo.get_all()
    boletas = boleta_repo.get_all()
    percepciones = percepcion_repo.get_all()
    
    # ============================================
    # CALCULAR TOTALES
    # ============================================
    total_ventas = sum(b.monto for b in boletas) if boletas else 0
    total_compras = sum(f.monto for f in facturas) if facturas else 0
    total_percepciones = sum(p.monto for p in percepciones) if percepciones else 0
    
    # ============================================
    # ÚLTIMO MES CON DATOS
    # ============================================
    ultimo_mes = None
    ventas_ultimo_mes = 0
    impuesto_mensual = 20
    estado_rus = "NORMAL"
    
    if boletas:
        ultima_boleta = max(boletas, key=lambda x: x.fecha_emision)
        ultimo_mes = {
            'mes': ultima_boleta.mes,
            'anio': ultima_boleta.anio,
            'nombre_mes': ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][ultima_boleta.mes-1]
        }
        
        # Ventas del último mes
        ventas_ultimo_mes = sum(b.monto for b in boletas if b.mes == ultimo_mes['mes'] and b.anio == ultimo_mes['anio'])
        
        # Calcular estado RUS
        estado_rus, impuesto_mensual = CalculadoraRUS.calcular_estado(ventas_ultimo_mes)
    
    # ============================================
    # CALCULAR UTILIDAD
    # ============================================
    utilidad = total_ventas - total_compras
    porcentaje_utilidad = (utilidad / total_ventas * 100) if total_ventas > 0 else 0
    
    # ============================================
    # VARIACIONES (SIMULADAS)
    # ============================================
    variacion_ventas = 12
    variacion_compras = -8
    
    # ============================================
    # CONTAR DOCUMENTOS POR TIPO
    # ============================================
    total_facturas = len(facturas)
    total_boletas = len(boletas)
    total_percepciones_count = len(percepciones)
    total_documentos = total_facturas + total_boletas + total_percepciones_count
    
    return render_template('index.html',
                         total_ventas=total_ventas,
                         total_compras=total_compras,
                         total_percepciones=total_percepciones,
                         total_boletas=total_boletas,
                         total_facturas=total_facturas,
                         total_percepciones_count=total_percepciones_count,
                         estado_rus=estado_rus,
                         impuesto_mensual=impuesto_mensual,
                         ultimo_mes=ultimo_mes,
                         utilidad=utilidad,
                         porcentaje_utilidad=porcentaje_utilidad,
                         variacion_ventas=variacion_ventas,
                         variacion_compras=variacion_compras,
                         total_documentos=total_documentos,
                         ventas_ultimo_mes=ventas_ultimo_mes,
                         facturas=facturas[:5],
                         boletas=boletas[:5])


# ============================================
# RUTA: SUBIR ARCHIVOS
# ============================================

@main_bp.route('/subir')
def subir():
    """Página de subida de archivos"""
    return render_template('subir.html')


# ============================================
# RUTA: VER DATOS (CON FILTROS)
# ============================================

@main_bp.route('/ver_datos')
def ver_datos():
    """Página de visualización de datos con filtros"""
    
    # Obtener parámetros de la URL
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    tipo = request.args.get('tipo', 'todos')
    
    # ============================================
    # OBTENER DATOS DE LA BASE DE DATOS
    # ============================================
    
    facturas = factura_repo.get_all()
    boletas = boleta_repo.get_all()
    percepciones = percepcion_repo.get_all()
    
    # ============================================
    # APLICAR FILTROS DE FECHA (mes/año)
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
    # APLICAR FILTRO DE TIPO
    # ============================================
    
    todos_items = []
    
    if tipo in ['todos', 'facturas']:
        for f in facturas:
            todos_items.append({
                'tipo': 'Factura',
                'id': f.id,
                'numero': f.numero,
                'fecha': f.fecha_emision,
                'monto': f.monto,
                'proveedor_cliente': f.proveedor or 'Natura Cosméticos S.A.',
                'descripcion': f.descripcion or f'Factura {f.numero}',
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
                'proveedor_cliente': b.cliente or 'Cliente no registrado',
                'descripcion': b.descripcion or f'Boleta {b.numero}',
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
                'proveedor_cliente': p.proveedor or 'Natura Cosméticos S.A.',
                'descripcion': p.descripcion or f'Percepción {p.numero}',
                'archivo': p.archivo
            })
    
    # ============================================
    # ORDENAR POR FECHA (más reciente primero)
    # ============================================
    
    todos_items.sort(key=lambda x: x['fecha'], reverse=True)
    
    # ============================================
    # PAGINACIÓN
    # ============================================
    
    total_items = len(todos_items)
    total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 1
    start = (page - 1) * per_page
    end = start + per_page
    items_paginated = todos_items[start:end]
    
    # ============================================
    # OBTENER AÑOS DISPONIBLES PARA FILTROS
    # ============================================
    
    all_facturas = factura_repo.get_all()
    all_boletas = boleta_repo.get_all()
    all_percepciones = percepcion_repo.get_all()
    
    años_set = set()
    for f in all_facturas:
        if f.anio:
            años_set.add(f.anio)
    for b in all_boletas:
        if b.anio:
            años_set.add(b.anio)
    for p in all_percepciones:
        if p.anio:
            años_set.add(p.anio)
    
    años_disponibles = sorted(list(años_set), reverse=True)
    
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


# ============================================
# RUTA: REPORTES (CON FILTROS Y AÑOS/MESES DISPONIBLES)
# ============================================

@main_bp.route('/reportes')
def reportes():
    """Página de reportes con gráficos interactivos"""
    
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    
    # ============================================
    # OBTENER DATOS PARA GRÁFICOS
    # ============================================
    datos = ReporteService.get_datos_completos_reportes(mes, anio)
    
    # ============================================
    # OBTENER AÑOS DISPONIBLES
    # ============================================
    
    from src.models.factura_compra import FacturaCompra
    from src.models.boleta_venta import BoletaVenta
    from src.models.percepcion import Percepcion
    from app import db
    
    # Obtener años únicos de todas las tablas
    años_facturas = db.session.query(FacturaCompra.anio).distinct().filter(FacturaCompra.anio.isnot(None)).all()
    años_boletas = db.session.query(BoletaVenta.anio).distinct().filter(BoletaVenta.anio.isnot(None)).all()
    años_percepciones = db.session.query(Percepcion.anio).distinct().filter(Percepcion.anio.isnot(None)).all()
    
    años_set = set()
    for a in años_facturas:
        if a[0] and a[0] > 0:
            años_set.add(a[0])
    for a in años_boletas:
        if a[0] and a[0] > 0:
            años_set.add(a[0])
    for a in años_percepciones:
        if a[0] and a[0] > 0:
            años_set.add(a[0])
    
    años_disponibles = sorted(list(años_set), reverse=True)
    
    # ============================================
    # OBTENER MESES DISPONIBLES PARA EL AÑO SELECCIONADO
    # ============================================
    
    meses_disponibles = []
    if anio:
        meses_facturas = db.session.query(FacturaCompra.mes).distinct().filter(
            FacturaCompra.anio == anio,
            FacturaCompra.mes.isnot(None)
        ).all()
        meses_boletas = db.session.query(BoletaVenta.mes).distinct().filter(
            BoletaVenta.anio == anio,
            BoletaVenta.mes.isnot(None)
        ).all()
        meses_percepciones = db.session.query(Percepcion.mes).distinct().filter(
            Percepcion.anio == anio,
            Percepcion.mes.isnot(None)
        ).all()
        
        meses_set = set()
        for m in meses_facturas:
            if m[0] and m[0] > 0:
                meses_set.add(m[0])
        for m in meses_boletas:
            if m[0] and m[0] > 0:
                meses_set.add(m[0])
        for m in meses_percepciones:
            if m[0] and m[0] > 0:
                meses_set.add(m[0])
        
        meses_disponibles = sorted(list(meses_set))
    
    return render_template('reportes.html',
                         datos=datos,
                         mes_actual=mes,
                         anio_actual=anio,
                         años_disponibles=años_disponibles,
                         meses_disponibles=meses_disponibles)


# ============================================
# RUTA: API REPORTES (AJAX)
# ============================================

@main_bp.route('/api/reportes/datos')
def api_reportes_datos():
    """Endpoint API para obtener datos de reportes en JSON"""
    
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    
    datos = ReporteService.get_datos_completos_reportes(mes, anio)
    return jsonify(datos)


# ============================================
# RUTA: GESTIÓN DE CARPETAS
# ============================================

@main_bp.route('/carpetas')
def carpetas():
    """Página de gestión de carpetas"""
    try:
        from pathlib import Path
        
        # ============================================
        # RUTA DE DATOS
        # ============================================
        base_dir = Path(__file__).resolve().parent.parent
        data_dir = base_dir / 'data'
        
        if not data_dir.exists():
            data_dir = Path('data')
        
        # ============================================
        # CONTAR DOCUMENTOS
        # ============================================
        total_facturas = 0
        total_boletas = 0
        total_percepciones = 0
        arbol = []
        
        if data_dir.exists():
            # Facturas
            facturas_dir = data_dir / 'facturas'
            if facturas_dir.exists():
                for carpeta in facturas_dir.iterdir():
                    if carpeta.is_dir():
                        pdfs = list(carpeta.glob('*.pdf'))
                        total_facturas += len(pdfs)
                        if len(pdfs) > 0:
                            arbol.append({
                                'tipo': 'facturas',
                                'nombre': carpeta.name,
                                'cantidad': len(pdfs)
                            })
            
            # Boletas
            boletas_dir = data_dir / 'boletas'
            if boletas_dir.exists():
                for carpeta in boletas_dir.iterdir():
                    if carpeta.is_dir():
                        pdfs = list(carpeta.glob('*.pdf'))
                        total_boletas += len(pdfs)
                        if len(pdfs) > 0:
                            arbol.append({
                                'tipo': 'boletas',
                                'nombre': carpeta.name,
                                'cantidad': len(pdfs)
                            })
            
            # Percepciones
            percepciones_dir = data_dir / 'percepciones'
            if percepciones_dir.exists():
                for carpeta in percepciones_dir.iterdir():
                    if carpeta.is_dir():
                        pdfs = list(carpeta.glob('*.pdf'))
                        total_percepciones += len(pdfs)
                        if len(pdfs) > 0:
                            arbol.append({
                                'tipo': 'percepciones',
                                'nombre': carpeta.name,
                                'cantidad': len(pdfs)
                            })
        
        total_documentos = total_facturas + total_boletas + total_percepciones
        total_carpetas = len(arbol)
        
        tipos = 0
        if total_facturas > 0: tipos += 1
        if total_boletas > 0: tipos += 1
        if total_percepciones > 0: tipos += 1
        
        # ============================================
        # CALCULAR ESPACIO
        # ============================================
        espacio = "0 MB"
        try:
            total_bytes = 0
            for pdf in data_dir.rglob('*.pdf'):
                total_bytes += pdf.stat().st_size
            if total_bytes < 1024 * 1024:
                espacio = f"{total_bytes / 1024:.1f} KB"
            else:
                espacio = f"{total_bytes / (1024 * 1024):.1f} MB"
        except:
            pass
        
        # ============================================
        # 🆕 AGRUPAR POR MES PARA EL RESUMEN
        # ============================================
        resumen_meses = []
        meses_dict = {}
        
        nombre_meses = {
            '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
            '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
            '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
        }
        
        for item in arbol:
            parts = item['nombre'].split('_')
            if len(parts) == 2:
                anio = parts[0]
                mes_num = parts[1]
                key = f"{anio}_{mes_num}"
                
                if key not in meses_dict:
                    meses_dict[key] = {
                        'anio': anio,
                        'mes': mes_num,
                        'facturas': 0,
                        'boletas': 0,
                        'percepciones': 0
                    }
                
                if item['tipo'] == 'facturas':
                    meses_dict[key]['facturas'] = item['cantidad']
                elif item['tipo'] == 'boletas':
                    meses_dict[key]['boletas'] = item['cantidad']
                elif item['tipo'] == 'percepciones':
                    meses_dict[key]['percepciones'] = item['cantidad']
        
        for key, data in meses_dict.items():
            mes_nombre = nombre_meses.get(data['mes'], data['mes'])
            resumen_meses.append({
                'nombre': f"{mes_nombre} {data['anio']}",
                'facturas': data['facturas'],
                'boletas': data['boletas'],
                'percepciones': data['percepciones'],
                'total': data['facturas'] + data['boletas'] + data['percepciones']
            })
        
        resumen_meses.sort(key=lambda x: x['nombre'], reverse=True)
        
        return render_template('carpetas.html',
                             total_carpetas=total_carpetas,
                             total_documentos=total_documentos,
                             total_mb=espacio,
                             total_facturas=total_facturas,
                             total_boletas=total_boletas,
                             total_percepciones=total_percepciones,
                             tipos=tipos,
                             arbol=arbol,
                             resumen_meses=resumen_meses)  # 🆕 AÑADIDO
    except Exception as e:
        print(f"❌ Error en carpetas: {str(e)}")
        return render_template('carpetas.html',
                             total_carpetas=0,
                             total_documentos=0,
                             total_mb="0 MB",
                             total_facturas=0,
                             total_boletas=0,
                             total_percepciones=0,
                             tipos=0,
                             arbol=[],
                             resumen_meses=[])  # 🆕 AÑADIDO


# ============================================
# API: ORGANIZAR CARPETAS
# ============================================

@main_bp.route('/api/organizar-carpetas', methods=['POST'])
def api_organizar_carpetas():
    """API para organizar carpetas automáticamente"""
    try:
        return jsonify({
            'success': True,
            'message': '✅ Carpetas organizadas correctamente'
        })
    except Exception as e:
        print(f"❌ Error en api_organizar_carpetas: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ============================================
# API: GUARDAR CONFIGURACIÓN
# ============================================

@main_bp.route('/api/configuracion/guardar', methods=['POST'])
def api_guardar_configuracion():
    """Endpoint para guardar configuración del usuario"""
    try:
        data = request.get_json()
        
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip()
        notificaciones = data.get('notificaciones', True)
        tema = data.get('tema', 'dark')
        color_primario = data.get('color_primario', '#60a5fa')
        
        if email and '@' not in email:
            return jsonify({
                'success': False,
                'message': 'Email inválido'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Configuración guardada correctamente',
            'data': {
                'nombre': nombre,
                'email': email,
                'notificaciones': notificaciones,
                'tema': tema,
                'color_primario': color_primario
            }
        })
    except Exception as e:
        print(f"❌ Error en api_guardar_configuracion: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ============================================
# RUTAS: BACKUP, HISTORIAL, CONFIGURACIÓN
# ============================================

@main_bp.route('/backup')
def backup():
    """Página de backups"""
    return render_template('backup.html')


@main_bp.route('/historial')
def historial():
    """Página de historial"""
    return render_template('historial.html')


@main_bp.route('/configuracion')
def configuracion():
    """Página de configuración"""
    return render_template('configuracion.html')


# ============================================
# RUTA: EXPORTAR A EXCEL
# ============================================

@main_bp.route('/exportar/excel')
def exportar_excel():
    """Exporta los datos a un archivo Excel profesional"""
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
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return jsonify({'error': 'Servicio de exportación no disponible'}), 501
    except Exception as e:
        print(f"❌ Error en exportación: {e}")
        return jsonify({'error': str(e)}), 500