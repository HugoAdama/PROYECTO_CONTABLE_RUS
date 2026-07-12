"""
Script de prueba para verificar la conexión a la base de datos
"""
import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.database.conexion import get_db, get_session, init_db
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion

def test_connection():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")
    
    try:
        # 1. Obtener sesión
        session = get_session()
        print("✅ Sesión obtenida correctamente")
        
        # 2. Contar registros
        facturas = session.query(FacturaCompra).count()
        boletas = session.query(BoletaVenta).count()
        percepciones = session.query(Percepcion).count()
        
        print(f"\n📊 Estadísticas de la base de datos:")
        print(f"  📄 Facturas: {facturas}")
        print(f"  📄 Boletas: {boletas}")
        print(f"  📄 Percepciones: {percepciones}")
        print(f"  📊 Total: {facturas + boletas + percepciones}")
        
        # 3. Verificar datos recientes
        if facturas > 0:
            ultima_factura = session.query(FacturaCompra).order_by(FacturaCompra.id.desc()).first()
            print(f"\n📄 Última factura:")
            print(f"  N°: {ultima_factura.numero_factura}")
            print(f"  Proveedor: {ultima_factura.proveedor}")
            print(f"  Total: S/ {ultima_factura.total_pagar:.2f}")
            print(f"  Mes/Año: {ultima_factura.mes}/{ultima_factura.anio}")
        
        if boletas > 0:
            ultima_boleta = session.query(BoletaVenta).order_by(BoletaVenta.id.desc()).first()
            print(f"\n🧾 Última boleta:")
            print(f"  N°: {ultima_boleta.numero_boleta}")
            print(f"  Cliente: {ultima_boleta.cliente}")
            print(f"  Total: S/ {ultima_boleta.total_pagar:.2f}")
            print(f"  Mes/Año: {ultima_boleta.mes}/{ultima_boleta.anio}")
        
        session.close()
        print("\n✅ Prueba completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()