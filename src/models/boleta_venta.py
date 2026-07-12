# src/models/boleta_venta.py
"""
📄 MODELO BOLETA VENTA - VERSIÓN COMPLETA
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from datetime import datetime
from src.database.conexion import Base

class BoletaVenta(Base):
    __tablename__ = 'boletas_venta'
    
    id = Column(Integer, primary_key=True)
    numero_boleta = Column(String(20), unique=True)
    serie = Column(String(10))
    fecha_emision = Column(Date)
    tipo_comprobante = Column(String(20))
    
    ruc_emisor = Column(String(11))
    nombre_emisor = Column(String(100))
    direccion_emisor = Column(String(200))
    
    nombre_cliente = Column(String(100))
    ruc_cliente = Column(String(11))
    direccion_cliente = Column(String(200))
    telefono_cliente = Column(String(20))
    
    monto_total = Column(Float)
    sub_total = Column(Float, default=0.0)
    igv = Column(Float, default=0.0)
    descuento = Column(Float, default=0.0)
    
    productos = Column(Text)
    cantidad_productos = Column(Integer, default=0)
    
    # ⭐ MES Y AÑO
    mes = Column(Integer)
    año = Column(Integer)
    
    descripcion = Column(String(500))
    observaciones = Column(Text)
    
    fecha_subida = Column(DateTime, default=datetime.now)
    estado = Column(String(20), default='pendiente')
    ruta_pdf = Column(String(255))
    
    def __repr__(self):
        return f"<Boleta {self.numero_boleta} - S/ {self.monto_total:.2f}>"
