"""Rutas de organización de carpetas con estadísticas reales."""
from collections import defaultdict
from pathlib import Path
from flask import current_app, render_template
from contable.api import main_bp
from src.database.models import Documento

@main_bp.route('/carpetas')
def carpetas():
    docs = Documento.query.order_by(Documento.fecha_emision.desc()).all()
    grouped = defaultdict(lambda: {'facturas':0,'boletas':0,'percepciones':0,'total':0})
    for doc in docs:
        key = doc.fecha_emision.strftime('%Y-%m')
        grouped[key][{'factura':'facturas','boleta':'boletas','percepcion':'percepciones'}[doc.tipo]] += 1
        grouped[key]['total'] += 1
    monthly = [{'mes':key, **values} for key,values in sorted(grouped.items(), reverse=True)]
    data_dir = Path(current_app.root_path).parent / 'data'
    size = sum(p.stat().st_size for p in data_dir.rglob('*') if p.is_file())
    folders = [{'nombre':key.replace('-','_'),'total':v['total'],'espacio':'Organizado'} for key,v in sorted(grouped.items(), reverse=True)]
    stats = {'carpetas':len(folders),'documentos':len(docs),'espacio':f'{size/1048576:.1f} MB','tipos':len({d.tipo for d in docs})}
    return render_template('carpetas.html', stats=stats, folders=folders, monthly=monthly)
