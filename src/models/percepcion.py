# src/models/percepcion.py
"""
📄 MODELO PERCEPCIÓN - VERSIÓN COMPLETA
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from datetime import datetime
from src.database.conexion import Base

class Percepcion(Base):
    __tablename__ = 'percepciones'
    
    id = Column(Integer, primary_key=True)
    
    numero_doc = Column(String(20))
    serie = Column(String(10))
    fecha_emision = Column(Date)
    factura_asociada = Column(String(20))
    proveedor = Column(String(100))
    ruc_proveedor = Column(String(11))
    
    monto = Column(Float)
    
    # ⭐ MES Y AÑO
    mes = Column(Integer)
    año = Column(Integer)
    
    ruta_pdf = Column(String(255))
    fecha_subida = Column(DateTime, default=datetime.now)
    observaciones = Column(Text)
    
    def __repr__(self):
        return f"<Percepcion {self.numero_doc} - S/ {self.monto:.2f}>"
