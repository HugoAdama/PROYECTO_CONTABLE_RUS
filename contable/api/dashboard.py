"""Rutas del dashboard, historial y respaldo."""
import logging
import shutil
from datetime import datetime
from pathlib import Path
from flask import current_app, render_template, send_from_directory
from contable.api import main_bp
from contable.services.ventas_service import VentasService
from src.database.models import Configuracion, Documento, Historial
logger=logging.getLogger(__name__); ventas_service=VentasService()

@main_bp.route('/')
def index():
    try:
        now=datetime.now(); latest=Documento.query.order_by(Documento.fecha_emision.desc()).first(); ref=latest.fecha_emision if latest else now.date()
        resumen=ventas_service.get_resumen_mensual(ref.year,ref.month); variacion=ventas_service.get_variacion_mensual(ref.year,ref.month); ultimos=ventas_service.get_ultimos_documentos(5)
        estado=resumen.get('estado_rus',{'estado':'NORMAL','mensaje':'Todo bien, sigue así','impuesto':20})
        return render_template('index.html',total_ventas=resumen.get('ventas',0),total_compras=resumen.get('compras',0),utilidad=resumen.get('utilidad',0),variacion_ventas=variacion.get('ventas',0),variacion_compras=variacion.get('compras',0),variacion_utilidad=variacion.get('utilidad',0),estado_rus=estado,impuesto_a_pagar=estado.get('impuesto',0),total_facturas=Documento.query.filter_by(tipo='factura').count(),total_boletas=Documento.query.filter_by(tipo='boleta').count(),total_percepciones=Documento.query.filter_by(tipo='percepcion').count(),ultimos_documentos=ultimos)
    except Exception as exc:
        logger.exception('Dashboard error'); return render_template('index.html',error=str(exc),total_ventas=0,total_compras=0,utilidad=0,variacion_ventas=0,variacion_compras=0,variacion_utilidad=0,estado_rus={'estado':'ERROR','mensaje':str(exc),'impuesto':0},impuesto_a_pagar=0,total_facturas=0,total_boletas=0,total_percepciones=0,ultimos_documentos=[])

@main_bp.route('/historial')
def historial(): return render_template('historial.html',historial=Historial.query.order_by(Historial.fecha.desc()).limit(50).all())

def _backup_dir():
    d=Path(current_app.root_path).parent/'data'/'backups'; d.mkdir(parents=True,exist_ok=True); return d

@main_bp.route('/backup')
def backup():
    backups=[]
    for p in sorted(_backup_dir().glob('*.db'),key=lambda x:x.stat().st_mtime,reverse=True): backups.append({'nombre':p.name,'fecha':datetime.fromtimestamp(p.stat().st_mtime).strftime('%d/%m/%Y %H:%M'),'tamano':f'{p.stat().st_size/1024:.1f} KB'})
    return render_template('backup.html',backups=backups)

@main_bp.route('/backup/crear')
def crear_backup():
    source=Path(current_app.root_path).parent/'data'/'rus.db'; name=f"backup_{datetime.now():%Y%m%d_%H%M%S}.db"; shutil.copy2(source,_backup_dir()/name); Historial.registrar('backup',f'Backup creado: {name}'); return send_from_directory(_backup_dir(),name,as_attachment=True)

@main_bp.route('/backup/descargar/<path:filename>')
def descargar_backup(filename): return send_from_directory(_backup_dir(),filename,as_attachment=True)
