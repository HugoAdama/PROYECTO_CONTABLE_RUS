# verificar_datos.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from src.database.models import Documento
from src.services.ventas_service import VentasService
from datetime import datetime

app = create_app()
with app.app_context():
    total = Documento.query.count()
    print(f'📊 Total documentos: {total}')
    
    if total > 0:
        print('\n📄 Documentos cargados:')
        for doc in Documento.query.all():
            print(f'  {doc.tipo}: {doc.numero} | S/{doc.monto_total:.2f} | {doc.fecha_emision}')
        
        now = datetime.now()
        r = VentasService().get_resumen_mensual(now.year, now.month)
        print(f'\n📊 RESUMEN DE {now.strftime("%B %Y")}:')
        print(f'  💰 Ventas: S/{r.get("ventas", 0):.2f}')
        print(f'  🛒 Compras: S/{r.get("compras", 0):.2f}')
        print(f'  📈 Utilidad: S/{r.get("utilidad", 0):.2f}')
        estado = r.get('estado_rus', {})
        print(f'  🏛️  Estado RUS: {estado.get("estado", "NORMAL")}')
        print(f'  💰 Impuesto: S/{estado.get("impuesto", 0):.2f}')
    else:
        print('⚠️  No hay datos cargados')
