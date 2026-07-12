# src/database/crear_tablas.py
from .conexion import engine, Base
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion

def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")

if __name__ == "__main__":
    crear_tablas()