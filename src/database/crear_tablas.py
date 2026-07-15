# src/database/crear_tablas.py
from app import db
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion

def crear_tablas():
    """Crea todas las tablas en la base de datos si no existen"""
    db.create_all()
    print("✅ Tablas creadas/verificadas correctamente")

if __name__ == "__main__":
    crear_tablas()