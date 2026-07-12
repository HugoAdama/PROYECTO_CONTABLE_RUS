# app/routes.py
"""
Rutas principales de la aplicación Flask
"""

from flask import Blueprint, render_template, request, jsonify
from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository
from src.database.conexion import get_db
from src.calculators.calculadora_rus import CalculadoraRUS
from src.utils.gestor_carpetas import GestorCarpetas
from src.utils.backup_manager import BackupManager

bp = Blueprint('main', __name__)


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
        
        total_ventas = sum(b.total_pagar for b in boletas) if boletas else 0
        total_compras = sum(f.total_pagar for f in facturas) if facturas else 0
        total_percepciones = sum(p.monto for p in percepciones) if percepciones else 0
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
            percepciones=percepciones
        )
    except Exception as e:
        print(f"Error en index: {e}")
        return render_template(
            'index.html',
            total_ventas=0,
            total_compras=0,
            total_percepciones=0,
            utilidad=0,
            impuesto=20,
            estado_rus={'estado': 'ok', 'mensaje': 'Error al cargar datos', 'color': 'warning', 'icono': '⚠️'},
            facturas=[],
            boletas=[],
            percepciones=[]
        )


@bp.route('/subir')
def subir():
    """Página de subida de archivos"""
    return render_template('subir.html')


@bp.route('/ver_datos')
def ver_datos():
    """Página de visualización de datos con filtros"""
    try:
        tipo = request.args.get('tipo', 'todas')
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
        
        facturas = []
        boletas = []
        percepciones = []
        
        if tipo == 'todas' or tipo == 'facturas':
            facturas = factura_repo.obtener_por_mes_anio(mes, anio)
        
        if tipo == 'todas' or tipo == 'boletas':
            boletas = boleta_repo.obtener_por_mes_anio(mes, anio)
        
        if tipo == 'todas' or tipo == 'percepciones':
            percepciones = percepcion_repo.obtener_por_mes_anio(mes, anio)
        
        total_facturas = sum(f.total_pagar for f in facturas) if facturas else 0
        total_boletas = sum(b.total_pagar for b in boletas) if boletas else 0
        total_percepciones = sum(p.monto for p in percepciones) if percepciones else 0
        
        total_registros = len(facturas) + len(boletas) + len(percepciones)
        
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
            total_registros=total_registros
        )
    except Exception as e:
        print(f"Error en ver_datos: {e}")
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
            total_registros=0
        )


@bp.route('/reportes')
def reportes():
    """Página de reportes y gráficos"""
    return render_template('reportes.html')


@bp.route('/carpetas')
def carpetas():
    """Página de gestión de carpetas"""
    try:
        gestor = GestorCarpetas()
        stats = gestor.obtener_estadisticas()
        return render_template('carpetas.html', stats=stats)
    except Exception as e:
        print(f"Error en carpetas: {e}")
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
        print(f"Error en backup: {e}")
        return render_template('backup.html', backups=[], stats={})


@bp.route('/historial')
def historial():
    """Página de historial de actividades"""
    return render_template('historial.html')


@bp.route('/configuracion')
def configuracion():
    """Página de configuración"""
    return render_template('configuracion.html')