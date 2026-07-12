# src/models/factura_compra.py
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from datetime import datetime
from src.database.conexion import Base

class FacturaCompra(Base):
    __tablename__ = 'facturas_compras'

    id = Column(Integer, primary_key=True)
    ruc_proveedor = Column(String(11))
    proveedor = Column(String(100))
    direccion_proveedor = Column(String(200))
    telefono_proveedor = Column(String(20))

    numero_factura = Column(String(20), unique=True)
    fecha_emision = Column(Date)
    fecha_vencimiento = Column(Date)
    tipo_comprobante = Column(String(20))
    serie = Column(String(10))

    sub_total = Column(Float)
    igv = Column(Float)
    total_con_descuento = Column(Float)
    percepcion = Column(Float)
    total_pagar = Column(Float)
    otros_cargos = Column(Float, default=0.0)
    descuento = Column(Float, default=0.0)

    productos = Column(Text)
    cantidad_productos = Column(Integer, default=0)

    mes = Column(Integer)
    anio = Column(Integer)

    ruta_pdf = Column(String(255))
    fecha_subida = Column(DateTime, default=datetime.now)
    estado = Column(String(20), default='pendiente')
    observaciones = Column(Text)

    def __repr__(self):
        return f"<Factura {self.numero_factura} - S/ {self.total_pagar:.2f}>"