# src/models/percepcion.py
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from datetime import datetime
from src.database.conexion import Base

class Percepcion(Base):
    __tablename__ = 'percepciones'

    id = Column(Integer, primary_key=True)
    numero_comprobante = Column(String(20))
    numero_documento = Column(String(20))
    proveedor = Column(String(100))
    ruc_proveedor = Column(String(11))

    fecha_emision = Column(Date)
    monto = Column(Float)
    porcentaje = Column(Float, default=2.0)
    monto_percibido = Column(Float)

    mes = Column(Integer)
    anio = Column(Integer)

    ruta_pdf = Column(String(255))
    fecha_subida = Column(DateTime, default=datetime.now)
    estado = Column(String(20), default='pendiente')

    def __repr__(self):
        return f"<Percepcion {self.numero_comprobante} - S/ {self.monto:.2f}>"