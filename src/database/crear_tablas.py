# src/database/crear_tablas.py
from contable.extensions import db
from contable.models.factura_compra import FacturaCompra
from contable.models.boleta_venta import BoletaVenta
from contable.models.percepcion import Percepcion

def crear_tablas():
    """Crea todas las tablas en la base de datos si no existen"""
    db.create_all()
    print("✅ Tablas creadas/verificadas correctamente")

if __name__ == "__main__":
    crear_tablas()