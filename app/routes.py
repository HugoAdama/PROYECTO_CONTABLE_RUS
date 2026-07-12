# app/routes.py
"""
Rutas principales de la aplicación Flask
Sistema de Control Financiero RUS v3.2
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository
from src.database.conexion import get_db
from src.calculators.calculadora_rus import CalculadoraRUS
from src.utils.gestor_carpetas import GestorCarpetas
from src.utils.backup_manager import BackupManager
import traceback
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)

# ============================================================
# CONFIGURACIÓN DE ARCHIVOS
# ============================================================

DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Verifica si el archivo tiene extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder(tipo, mes, anio):
    """
    Obtiene la carpeta de subida según el tipo, mes y año
    Estructura: data/{tipo}/{anio}_{mes}/
    Ejemplo: data/boletas/2026_05/
    """
    carpetas = {
        'factura': 'facturas',
        'boleta': 'boletas',
        'percepcion': 'percepciones',
        'temporal': 'temporal'
    }
    
    nombre_carpeta = carpetas.get(tipo, 'pdfs')
    carpeta_mes = f"{anio}_{str(mes).zfill(2)}"
    
    ruta = os.path.join(DATA_FOLDER, nombre_carpeta, carpeta_mes)
    
    # Crear la carpeta si no existe
    if not os.path.exists(ruta):
        os.makedirs(ruta, exist_ok=True)
        print(f"📁 Carpeta creada: {ruta}")
    
    return ruta

def ensure_upload_folder():
    """Asegura que la carpeta base de uploads exista (compatibilidad)"""
    upload_folder = os.path.join(DATA_FOLDER, 'pdfs')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

# ============================================================
# RUTAS PRINCIPALES
# ============================================================

@bp.route('/')
def index():
    """Página de inicio - Dashboard principal"""
    try:
        session = get_db()
        
        factura_repo = FacturaRepository(session)
        boleta_repo = BoletaRepository(session)
        percepcion_repo = PercepcionRepository(session)
        
        mes = 5
        anio = 2026
        
        facturas = factura_repo.obtener_por_mes_anio(mes, anio)
        boletas = boleta_repo.obtener_por_mes_anio(mes, anio)
        percepciones = percepcion_repo.obtener_por_mes_anio(mes, anio)
        
        # ✅ Manejar valores None (null) en la base de datos
        total_ventas = sum(b.total_pagar or 0 for b in boletas) if boletas else 0
        total_compras = sum(f.total_pagar or 0 for f in facturas) if facturas else 0
        total_percepciones = sum(p.monto or 0 for p in percepciones) if percepciones else 0
        utilidad = total_ventas - total_compras
        
        calc = CalculadoraRUS(total_ventas, mes=mes, anio=anio)
        impuesto = calc.calcular_impuesto()
        estado_rus = calc.obtener_estado()
        
        session.close()
        
        return render_template(
            'index.html',
            total_ventas=total_ventas,
            total_compras=total_compras,
            total_percepciones=total_percepciones,
            utilidad=utilidad,
            impuesto=impuesto,
            estado_rus=estado_rus,
            facturas=facturas,
            boletas=boletas,
            percepciones=percepciones,
            mes_actual=mes,
            anio_actual=anio
        )
    except Exception as e:
        print(f"❌ Error en index: {e}")
        traceback.print_exc()
        return render_template(
            'index.html',
            total_ventas=0,
            total_compras=0,
            total_percepciones=0,
            utilidad=0,
            impuesto=20,
            estado_rus={'estado': 'error', 'mensaje': 'Error al cargar datos', 'color': 'danger', 'icono': '❌'},
            facturas=[],
            boletas=[],
            percepciones=[],
            mes_actual=5,
            anio_actual=2026
        )


@bp.route('/subir')
def subir():
    """Página de subida de archivos - Muestra todos los documentos procesados"""
    try:
        session = get_db()
        factura_repo = FacturaRepository(session)
        boleta_repo = BoletaRepository(session)
        percepcion_repo = PercepcionRepository(session)
        
        mes = 5
        anio = 2026
        
        facturas = factura_repo.obtener_por_mes_anio(mes, anio)
        boletas = boleta_repo.obtener_por_mes_anio(mes, anio)
        percepciones = percepcion_repo.obtener_por_mes_anio(mes, anio)
        
        # Ordenar por ID descendente (los más nuevos primero)
        facturas = sorted(facturas, key=lambda x: x.id, reverse=True)
        boletas = sorted(boletas, key=lambda x: x.id, reverse=True)
        percepciones = sorted(percepciones, key=lambda x: x.id, reverse=True)
        
        total_documentos = len(facturas) + len(boletas) + len(percepciones)
        
        session.close()
        
        return render_template(
            'subir.html',
            facturas=facturas,
            boletas=boletas,
            percepciones=percepciones,
            total_documentos=total_documentos,
            mes_actual=mes,
            anio_actual=anio
        )
    except Exception as e:
        print(f"❌ Error en subir: {e}")
        traceback.print_exc()
        return render_template(
            'subir.html',
            facturas=[],
            boletas=[],
            percepciones=[],
            total_documentos=0,
            mes_actual=5,
            anio_actual=2026
        )


@bp.route('/ver_datos')
def ver_datos():
    """Página de visualización de datos con filtros"""
    try:
        tipo = request.args.get('tipo', 'todas')
        mes_str = request.args.get('mes', '5')
        anio_str = request.args.get('anio', '2026')
        
        try:
            mes = int(mes_str)
            anio = int(anio_str)
        except ValueError:
            mes = 5
            anio = 2026
        
        session = get_db()
        
        factura_repo = FacturaRepository(session)
        boleta_repo = BoletaRepository(session)
        percepcion_repo = PercepcionRepository(session)
        
        facturas = []
        boletas = []
        percepciones = []
        
        if tipo == 'todas' or tipo == 'facturas':
            facturas = factura_repo.obtener_por_mes_anio(mes, anio)
        
        if tipo == 'todas' or tipo == 'boletas':
            boletas = boleta_repo.obtener_por_mes_anio(mes, anio)
        
        if tipo == 'todas' or tipo == 'percepciones':
            percepciones = percepcion_repo.obtener_por_mes_anio(mes, anio)
        
        # ✅ Manejar valores None (null) en la base de datos
        total_facturas = sum(f.total_pagar or 0 for f in facturas) if facturas else 0
        total_boletas = sum(b.total_pagar or 0 for b in boletas) if boletas else 0
        total_percepciones = sum(p.monto or 0 for p in percepciones) if percepciones else 0
        total_registros = len(facturas) + len(boletas) + len(percepciones)
        total_general = total_facturas + total_boletas + total_percepciones
        
        session.close()
        
        return render_template(
            'ver_datos.html',
            tipo=tipo,
            mes=mes,
            anio=anio,
            facturas=facturas,
            boletas=boletas,
            percepciones=percepciones,
            total_facturas=total_facturas,
            total_boletas=total_boletas,
            total_percepciones=total_percepciones,
            total_registros=total_registros,
            total_general=total_general
        )
    except Exception as e:
        print(f"❌ Error en ver_datos: {e}")
        traceback.print_exc()
        return render_template(
            'ver_datos.html',
            tipo='todas',
            mes=5,
            anio=2026,
            facturas=[],
            boletas=[],
            percepciones=[],
            total_facturas=0,
            total_boletas=0,
            total_percepciones=0,
            total_registros=0,
            total_general=0
        )


@bp.route('/reportes')
def reportes():
    """Página de reportes y gráficos"""
    try:
        mes = request.args.get('mes', '5')
        anio = request.args.get('anio', '2026')
        
        try:
            mes = int(mes)
            anio = int(anio)
        except ValueError:
            mes = 5
            anio = 2026
        
        session = get_db()
        
        factura_repo = FacturaRepository(session)
        boleta_repo = BoletaRepository(session)
        percepcion_repo = PercepcionRepository(session)
        
        facturas = factura_repo.obtener_por_mes_anio(mes, anio)
        boletas = boleta_repo.obtener_por_mes_anio(mes, anio)
        percepciones = percepcion_repo.obtener_por_mes_anio(mes, anio)
        
        # ✅ Manejar valores None (null) en la base de datos
        total_ventas = sum(b.total_pagar or 0 for b in boletas) if boletas else 0
        total_compras = sum(f.total_pagar or 0 for f in facturas) if facturas else 0
        total_percepciones = sum(p.monto or 0 for p in percepciones) if percepciones else 0
        utilidad = total_ventas - total_compras
        
        calc = CalculadoraRUS(total_ventas, mes=mes, anio=anio)
        impuesto = calc.calcular_impuesto()
        
        session.close()
        
        return render_template(
            'reportes.html',
            mes=mes,
            anio=anio,
            total_ventas=total_ventas,
            total_compras=total_compras,
            total_percepciones=total_percepciones,
            utilidad=utilidad,
            impuesto=impuesto,
            facturas=facturas,
            boletas=boletas,
            percepciones=percepciones
        )
    except Exception as e:
        print(f"❌ Error en reportes: {e}")
        traceback.print_exc()
        return render_template(
            'reportes.html',
            mes=5,
            anio=2026,
            total_ventas=0,
            total_compras=0,
            total_percepciones=0,
            utilidad=0,
            impuesto=0,
            facturas=[],
            boletas=[],
            percepciones=[]
        )


@bp.route('/carpetas')
def carpetas():
    """Página de gestión de carpetas"""
    try:
        gestor = GestorCarpetas()
        stats = gestor.obtener_estadisticas()
        return render_template('carpetas.html', stats=stats)
    except Exception as e:
        print(f"❌ Error en carpetas: {e}")
        traceback.print_exc()
        return render_template('carpetas.html', stats={})


@bp.route('/backup')
def backup():
    """Página de copias de seguridad"""
    try:
        backup_manager = BackupManager()
        backups = backup_manager.listar_backups()
        stats = backup_manager.obtener_estadisticas()
        return render_template('backup.html', backups=backups, stats=stats)
    except Exception as e:
        print(f"❌ Error en backup: {e}")
        traceback.print_exc()
        return render_template('backup.html', backups=[], stats={})


@bp.route('/historial')
def historial():
    """Página de historial de actividades"""
    try:
        return render_template('historial.html')
    except Exception as e:
        print(f"❌ Error en historial: {e}")
        traceback.print_exc()
        return render_template('historial.html')


@bp.route('/configuracion')
def configuracion():
    """Página de configuración"""
    try:
        return render_template('configuracion.html')
    except Exception as e:
        print(f"❌ Error en configuracion: {e}")
        traceback.print_exc()
        return render_template('configuracion.html')


# ============================================================
# API DE SUBIDA DE ARCHIVOS CON DETECCIÓN AUTOMÁTICA
# ============================================================

@bp.route('/api/subir_pdf', methods=['POST'])
def api_subir_pdf():
    """
    API para subir y procesar archivos PDF con detección automática
    """
    try:
        from src.extractors import FacturaExtractor, BoletaExtractor, PercepcionExtractor, DetectorExtractor
        import pdfplumber
        import io
        
        # Validar que haya archivos
        if 'archivos' not in request.files:
            return jsonify({'success': False, 'error': 'No se enviaron archivos'}), 400
        
        archivos = request.files.getlist('archivos')
        if not archivos or archivos[0].filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionaron archivos'}), 400
        
        # Obtener parámetros (lo que seleccionó la usuaria)
        tipo_seleccionado = request.form.get('tipo', 'factura')
        mes_seleccionado = request.form.get('mes', '5')
        anio_seleccionado = request.form.get('anio', '2026')
        
        try:
            mes_seleccionado = int(mes_seleccionado)
            anio_seleccionado = int(anio_seleccionado)
        except ValueError:
            mes_seleccionado = 5
            anio_seleccionado = 2026
        
        # Validar tipo seleccionado
        if tipo_seleccionado not in ['factura', 'boleta', 'percepcion']:
            return jsonify({'success': False, 'error': f'Tipo de documento no soportado: {tipo_seleccionado}'}), 400
        
        session = get_db()
        factura_repo = FacturaRepository(session)
        boleta_repo = BoletaRepository(session)
        percepcion_repo = PercepcionRepository(session)
        
        procesados = []
        errores = []
        advertencias = []
        carpeta_destino = None
        
        for archivo in archivos:
            try:
                # Validar extensión
                if not allowed_file(archivo.filename):
                    errores.append(f"❌ {archivo.filename}: Formato no permitido (solo PDF)")
                    continue
                
                # Guardar archivo temporalmente para analizar
                filename = secure_filename(archivo.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nombre_guardado = f"{timestamp}_{filename}"
                
                # ============================================================
                # PASO 1: GUARDAR TEMPORALMENTE PARA ANALIZAR
                # ============================================================
                carpeta_temporal = get_upload_folder('temporal', 5, 2026)
                ruta_temporal = os.path.join(carpeta_temporal, nombre_guardado)
                archivo.save(ruta_temporal)
                
                # ============================================================
                # PASO 2: DETECTAR TIPO REAL Y FECHA DEL DOCUMENTO
                # ============================================================
                detector = DetectorExtractor()
                resultado_deteccion = detector.extraer(ruta_temporal)
                
                tipo_real = resultado_deteccion.get('tipo_detectado', 'desconocido')
                fecha_detectada = resultado_deteccion.get('fecha_detectada')
                
                if fecha_detectada:
                    mes_real, anio_real = fecha_detectada
                else:
                    mes_real, anio_real = None, None
                
                # ============================================================
                # PASO 3: DECIDIR QUÉ TIPO Y FECHA USAR
                # ============================================================
                # Tipo: si es desconocido, usar el seleccionado
                if tipo_real == 'desconocido':
                    tipo_usar = tipo_seleccionado
                    advertencias.append(f"⚠️ No se pudo detectar el tipo de '{archivo.filename}'. Se usará '{tipo_seleccionado}'.")
                else:
                    tipo_usar = tipo_real
                    if tipo_real != tipo_seleccionado:
                        advertencias.append(f"🔍 Detectamos que '{archivo.filename}' es una {tipo_real}. Se guardará en la carpeta correcta.")
                
                # Fecha: si no se detectó, usar la seleccionada
                if mes_real is None or anio_real is None:
                    mes_usar = mes_seleccionado
                    anio_usar = anio_seleccionado
                else:
                    mes_usar = mes_real
                    anio_usar = anio_real
                    if mes_real != mes_seleccionado or anio_real != anio_seleccionado:
                        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                        advertencias.append(
                            f"📅 Detectamos que '{archivo.filename}' es de {meses[mes_real-1]} {anio_real}. "
                            f"Se guardará en la carpeta correcta."
                        )
                
                # ============================================================
                # PASO 4: MOVER A LA CARPETA CORRECTA
                # ============================================================
                carpeta_destino = get_upload_folder(tipo_usar, mes_usar, anio_usar)
                ruta_guardado = os.path.join(carpeta_destino, nombre_guardado)
                
                # Mover el archivo de la carpeta temporal a la definitiva
                os.rename(ruta_temporal, ruta_guardado)
                print(f"✅ Archivo guardado en: {ruta_guardado}")
                
                # ============================================================
                # PASO 5: PROCESAR CON EL EXTRACTOR CORRECTO
                # ============================================================
                if tipo_usar == 'factura':
                    extractor = FacturaExtractor()
                    documento = extractor.extraer(ruta_guardado)
                    if documento:
                        from src.models.factura_compra import FacturaCompra
                        factura = FacturaCompra()
                        
                        for key, value in documento.items():
                            if hasattr(factura, key):
                                if key == 'fecha_emision' and isinstance(value, str):
                                    try:
                                        factura.fecha_emision = datetime.strptime(value, '%Y-%m-%d').date()
                                    except ValueError:
                                        factura.fecha_emision = datetime.now().date()
                                else:
                                    setattr(factura, key, value)
                        
                        factura.mes = mes_usar
                        factura.anio = anio_usar
                        factura.fecha_subida = datetime.now()
                        factura_repo.guardar(factura)
                        
                        procesados.append({
                            'tipo': 'factura',
                            'numero': getattr(factura, 'numero_factura', 'DESCONOCIDO'),
                            'proveedor': getattr(factura, 'proveedor', 'DESCONOCIDO'),
                            'total': getattr(factura, 'total_pagar', 0),
                            'archivo': archivo.filename,
                            'mes': mes_usar,
                            'anio': anio_usar
                        })
                    else:
                        errores.append(f"❌ {archivo.filename}: Error al extraer datos de factura")
                
                elif tipo_usar == 'boleta':
                    extractor = BoletaExtractor()
                    documento = extractor.extraer(ruta_guardado)
                    if documento:
                        from src.models.boleta_venta import BoletaVenta
                        boleta = BoletaVenta()
                        
                        for key, value in documento.items():
                            if hasattr(boleta, key):
                                if key == 'fecha_emision' and isinstance(value, str):
                                    try:
                                        boleta.fecha_emision = datetime.strptime(value, '%Y-%m-%d').date()
                                    except ValueError:
                                        boleta.fecha_emision = datetime.now().date()
                                else:
                                    setattr(boleta, key, value)
                        
                        boleta.mes = mes_usar
                        boleta.anio = anio_usar
                        boleta.fecha_subida = datetime.now()
                        boleta_repo.guardar(boleta)
                        
                        procesados.append({
                            'tipo': 'boleta',
                            'numero': getattr(boleta, 'numero_boleta', 'DESCONOCIDO'),
                            'cliente': getattr(boleta, 'cliente', 'DESCONOCIDO'),
                            'total': getattr(boleta, 'total_pagar', 0),
                            'archivo': archivo.filename,
                            'mes': mes_usar,
                            'anio': anio_usar
                        })
                    else:
                        errores.append(f"❌ {archivo.filename}: Error al extraer datos de boleta")
                
                elif tipo_usar == 'percepcion':
                    extractor = PercepcionExtractor()
                    documento = extractor.extraer(ruta_guardado)
                    if documento:
                        from src.models.percepcion import Percepcion
                        percepcion = Percepcion()
                        
                        for key, value in documento.items():
                            if hasattr(percepcion, key):
                                if key == 'fecha_emision' and isinstance(value, str):
                                    try:
                                        percepcion.fecha_emision = datetime.strptime(value, '%Y-%m-%d').date()
                                    except ValueError:
                                        percepcion.fecha_emision = datetime.now().date()
                                else:
                                    setattr(percepcion, key, value)
                        
                        percepcion.mes = mes_usar
                        percepcion.anio = anio_usar
                        percepcion.fecha_subida = datetime.now()
                        percepcion_repo.guardar(percepcion)
                        
                        procesados.append({
                            'tipo': 'percepcion',
                            'numero': getattr(percepcion, 'numero_comprobante', 'DESCONOCIDO'),
                            'proveedor': getattr(percepcion, 'proveedor', 'DESCONOCIDO'),
                            'monto': getattr(percepcion, 'monto', 0),
                            'archivo': archivo.filename,
                            'mes': mes_usar,
                            'anio': anio_usar
                        })
                    else:
                        errores.append(f"❌ {archivo.filename}: Error al extraer datos de percepción")
                
            except Exception as e:
                errores.append(f"❌ {archivo.filename}: {str(e)}")
                print(f"Error procesando {archivo.filename}: {e}")
                traceback.print_exc()
        
        session.close()
        
        return jsonify({
            'success': True,
            'procesados': procesados,
            'errores': errores,
            'advertencias': advertencias,
            'total_procesados': len(procesados),
            'total_errores': len(errores),
            'mensaje': f'Se procesaron {len(procesados)} archivos correctamente' + (f' ({len(errores)} errores)' if errores else ''),
            'carpeta': carpeta_destino or 'No definida'
        })
        
    except Exception as e:
        print(f"❌ Error en api_subir_pdf: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# API PARA EL FRONTEND (AJAX)
# ============================================================

@bp.route('/api/filtrar_datos', methods=['GET'])
def api_filtrar_datos():
    """API para filtrar datos desde el frontend"""
    try:
        tipo = request.args.get('tipo', 'todas')
        mes = request.args.get('mes', '5')
        anio = request.args.get('anio', '2026')
        
        try:
            mes = int(mes)
            anio = int(anio)
        except ValueError:
            return jsonify({'error': 'Parámetros inválidos'}), 400
        
        session = get_db()
        
        factura_repo = FacturaRepository(session)
        boleta_repo = BoletaRepository(session)
        percepcion_repo = PercepcionRepository(session)
        
        response = {
            'facturas': [],
            'boletas': [],
            'percepciones': [],
            'totales': {
                'facturas': 0,
                'boletas': 0,
                'percepciones': 0,
                'general': 0
            }
        }
        
        if tipo == 'todas' or tipo == 'facturas':
            facturas = factura_repo.obtener_por_mes_anio(mes, anio)
            response['facturas'] = [f.to_dict() for f in facturas]
            response['totales']['facturas'] = sum(f.total_pagar or 0 for f in facturas)
        
        if tipo == 'todas' or tipo == 'boletas':
            boletas = boleta_repo.obtener_por_mes_anio(mes, anio)
            response['boletas'] = [b.to_dict() for b in boletas]
            response['totales']['boletas'] = sum(b.total_pagar or 0 for b in boletas)
        
        if tipo == 'todas' or tipo == 'percepciones':
            percepciones = percepcion_repo.obtener_por_mes_anio(mes, anio)
            response['percepciones'] = [p.to_dict() for p in percepciones]
            response['totales']['percepciones'] = sum(p.monto or 0 for p in percepciones)
        
        response['totales']['general'] = (
            response['totales']['facturas'] + 
            response['totales']['boletas'] + 
            response['totales']['percepciones']
        )
        response['total_registros'] = (
            len(response['facturas']) + 
            len(response['boletas']) + 
            len(response['percepciones'])
        )
        
        session.close()
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Error en api_filtrar_datos: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/estadisticas', methods=['GET'])
def api_estadisticas():
    """API para obtener estadísticas rápidas"""
    try:
        mes = request.args.get('mes', '5')
        anio = request.args.get('anio', '2026')
        
        try:
            mes = int(mes)
            anio = int(anio)
        except ValueError:
            return jsonify({'error': 'Parámetros inválidos'}), 400
        
        session = get_db()
        
        factura_repo = FacturaRepository(session)
        boleta_repo = BoletaRepository(session)
        percepcion_repo = PercepcionRepository(session)
        
        facturas = factura_repo.obtener_por_mes_anio(mes, anio)
        boletas = boleta_repo.obtener_por_mes_anio(mes, anio)
        percepciones = percepcion_repo.obtener_por_mes_anio(mes, anio)
        
        total_ventas = sum(b.total_pagar or 0 for b in boletas) if boletas else 0
        total_compras = sum(f.total_pagar or 0 for f in facturas) if facturas else 0
        total_percepciones = sum(p.monto or 0 for p in percepciones) if percepciones else 0
        utilidad = total_ventas - total_compras
        
        calc = CalculadoraRUS(total_ventas, mes=mes, anio=anio)
        impuesto = calc.calcular_impuesto()
        estado = calc.obtener_estado()
        
        session.close()
        
        return jsonify({
            'total_ventas': total_ventas,
            'total_compras': total_compras,
            'total_percepciones': total_percepciones,
            'utilidad': utilidad,
            'impuesto': impuesto,
            'estado_rus': estado,
            'mes': mes,
            'anio': anio,
            'total_registros': len(facturas) + len(boletas) + len(percepciones),
            'total_facturas': len(facturas),
            'total_boletas': len(boletas),
            'total_percepciones': len(percepciones)
        })
    
    except Exception as e:
        print(f"❌ Error en api_estadisticas: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================
# API PARA BACKUP
# ============================================================

@bp.route('/api/crear_backup', methods=['POST'])
def api_crear_backup():
    """Crea una copia de seguridad de la base de datos"""
    try:
        backup_manager = BackupManager()
        resultado = backup_manager.crear_backup()
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Error en api_crear_backup: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/restaurar_backup', methods=['POST'])
def api_restaurar_backup():
    """Restaura una copia de seguridad"""
    try:
        nombre_backup = request.json.get('nombre')
        if not nombre_backup:
            return jsonify({'success': False, 'error': 'Nombre de backup requerido'}), 400
        
        backup_manager = BackupManager()
        resultado = backup_manager.restaurar_backup(nombre_backup)
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Error en api_restaurar_backup: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/listar_backups', methods=['GET'])
def api_listar_backups():
    """Lista los backups disponibles"""
    try:
        backup_manager = BackupManager()
        backups = backup_manager.listar_backups()
        return jsonify({'success': True, 'backups': backups})
    except Exception as e:
        print(f"❌ Error en api_listar_backups: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# MANEJO DE ERRORES GLOBAL
# ============================================================

@bp.errorhandler(404)
def page_not_found(e):
    """Manejo de error 404"""
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_server_error(e):
    """Manejo de error 500"""
    return render_template('500.html'), 500