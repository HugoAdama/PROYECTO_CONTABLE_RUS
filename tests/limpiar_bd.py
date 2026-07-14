# limpiar_bd.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion

app = create_app()

with app.app_context():
    print("🧹 Limpiando base de datos...")
    
    # Eliminar todos los registros
    boletas = BoletaVenta.query.delete()
    facturas = FacturaCompra.query.delete()
    percepciones = Percepcion.query.delete()
    
    db.session.commit()
    
    print(f"  ✅ Eliminadas todas las boletas")
    print(f"  ✅ Eliminadas todas las facturas")
    print(f"  ✅ Eliminadas todas las percepciones")
    print("✅ Base de datos limpia")