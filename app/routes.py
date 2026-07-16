# app/routes.py
# ============

import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename

from src.database.models import Documento, Historial, Configuracion
from src.database.conexion import db
from contable.services.ventas_service import VentasService

logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)
ventas_service = VentasService()


# ============================================
# VISTAS PRINCIPALES
# ============================================

@main_bp.route('/')
def index():
    try:
        now = datetime.now()
        resumen = ventas_service.get_resumen_mensual(now.year, now.month)
        variacion = ventas_service.get_variacion_mensual(now.year, now.month)
        ultimos = ventas_service.get_ultimos_documentos(5)
        
        total_facturas = Documento.query.filter_by(tipo='factura').count()
        total_boletas = Documento.query.filter_by(tipo='boleta').count()
        total_percepciones = Documento.query.filter_by(tipo='percepcion').count()
        
        config = {
            'nombre_negocio': Configuracion.get('nombre_negocio', 'Maria Boutique'),
            'color_primario': Configuracion.get('color_primario', '#4A90D9'),
        }
        
        estado_rus = resumen.get('estado_rus', {
            'estado': 'NORMAL',
            'mensaje': 'Todo bien, sigue así',
            'icon': '✅',
            'impuesto': 20.00
        })
        
        return render_template('index.html',
            config=config,
            total_ventas=resumen.get('ventas', 0),
            total_compras=resumen.get('compras', 0),
            utilidad=resumen.get('utilidad', 0),
            percepciones=resumen.get('percepciones', 0),
            variacion_ventas=variacion.get('ventas', 0),
            variacion_compras=variacion.get('compras', 0),
            variacion_utilidad=variacion.get('utilidad', 0),
            estado_rus=estado_rus,
            impuesto_a_pagar=estado_rus.get('impuesto', 0),
            total_documentos=resumen.get('total_documentos', 0),
            total_facturas=total_facturas,
            total_boletas=total_boletas,
            total_percepciones=total_percepciones,
            ultimos_documentos=ultimos,
            mes_actual=now.strftime('%B %Y')
        )
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('index.html', error=str(e))


@main_bp.route('/subir')
def subir():
    return render_template('subir.html')


@main_bp.route('/ver_datos')
def ver_datos():
    try:
        year = request.args.get('year', type=int, default=datetime.now().year)
        month = request.args.get('month', type=int, default=datetime.now().month)
        return render_template('ver_datos.html',
            documentos=ventas_service.get_documentos_mes(year, month),
            resumen=ventas_service.get_resumen_mensual(year, month),
            year=year, month=month)
    except Exception as e:
        return render_template('ver_datos.html', error=str(e))


@main_bp.route('/reportes')
def reportes():
    try:
        now = datetime.now()
        resumen = ventas_service.get_resumen_mensual(now.year, now.month)
        meses, ventas_meses, compras_meses = [], [], []
        for i in range(6):
            m = now.month - i
            a = now.year
            if m <= 0:
                m += 12
                a -= 1
            datos = ventas_service.get_resumen_mensual(a, m)
            meses.append(f"{a}-{m:02d}")
            ventas_meses.append(datos.get('ventas', 0))
            compras_meses.append(datos.get('compras', 0))
        return render_template('reportes.html',
            resumen=resumen,
            meses=meses[::-1],
            ventas_meses=ventas_meses[::-1],
            compras_meses=compras_meses[::-1])
    except Exception as e:
        return render_template('reportes.html', error=str(e))


@main_bp.route('/configuracion')
def configuracion():
    try:
        config = {
            'nombre_negocio': Configuracion.get('nombre_negocio', 'Maria Boutique'),
            'color_primario': Configuracion.get('color_primario', '#4A90D9'),
            'limite_rus': Configuracion.get('limite_rus', '8000'),
            'impuesto_normal': Configuracion.get('impuesto_normal', '20'),
            'impuesto_alerta': Configuracion.get('impuesto_alerta', '50'),
        }
        return render_template('configuracion.html', config=config)
    except Exception as e:
        return render_template('configuracion.html', error=str(e))


@main_bp.route('/historial')
def historial():
    try:
        return render_template('historial.html',
            historial=Historial.query.order_by(Historial.fecha.desc()).limit(50).all())
    except Exception as e:
        return render_template('historial.html', error=str(e))


@main_bp.route('/backup')
def backup():
    return render_template('backup.html')


@main_bp.route('/carpetas')
def carpetas():
    return render_template('carpetas.html')


# ============================================
# API ENDPOINTS
# ============================================

@main_bp.route('/api/upload', methods=['POST'])
def api_upload():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó archivo'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Nombre vacío'}), 400
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'message': 'Solo PDFs'}), 400
        
        filename = secure_filename(file.filename)
        upload_dir = current_app.config['UPLOAD_FOLDER']
        file_path = upload_dir / filename
        counter = 1
        original = file_path
        while file_path.exists():
            file_path = upload_dir / f"{original.stem}_{counter}{original.suffix}"
            counter += 1
        file.save(str(file_path))
        result = ventas_service.procesar_archivo(file_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/config', methods=['POST'])
def api_config():
    try:
        data = request.get_json()
        for key, value in data.items():
            if key in ['nombre_negocio', 'color_primario', 'limite_rus', 'impuesto_normal', 'impuesto_alerta']:
                Configuracion.set(key, value)
        Historial.registrar('config', 'Configuración actualizada')
        return jsonify({'success': True, 'message': 'Configuración guardada'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/documentos', methods=['GET'])
def api_documentos():
    try:
        tipo = request.args.get('tipo')
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        query = Documento.query
        if tipo:
            query = query.filter_by(tipo=tipo)
        if fecha_desde:
            query = query.filter(Documento.fecha_emision >= fecha_desde)
        if fecha_hasta:
            query = query.filter(Documento.fecha_emision <= fecha_hasta)
        documentos = query.order_by(Documento.fecha_emision.desc()).limit(100).all()
        return jsonify({'success': True, 'documentos': [doc.to_dict() for doc in documentos]})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
