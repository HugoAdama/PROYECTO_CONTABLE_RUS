# src/models/boleta_venta.py
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from datetime import datetime
from src.database.conexion import Base

class BoletaVenta(Base):
    __tablename__ = 'boletas_venta'

    id = Column(Integer, primary_key=True)
    ruc_cliente = Column(String(11))
    cliente = Column(String(100))
    direccion_cliente = Column(String(200))

    numero_boleta = Column(String(20), unique=True)
    fecha_emision = Column(Date)
    tipo_comprobante = Column(String(20))
    serie = Column(String(10))

    sub_total = Column(Float)
    igv = Column(Float)
    total_con_descuento = Column(Float)
    total_pagar = Column(Float)
    descuento = Column(Float, default=0.0)

    productos = Column(Text)
    cantidad_productos = Column(Integer, default=0)

    mes = Column(Integer)
    anio = Column(Integer)

    ruta_pdf = Column(String(255))
    fecha_subida = Column(DateTime, default=datetime.now)
    estado = Column(String(20), default='pendiente')

    def __repr__(self):
        return f"<Boleta {self.numero_boleta} - S/ {self.total_pagar:.2f}>"