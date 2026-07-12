"""
Modelo SQLAlchemy para la tabla percepciones
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from src.database.conexion import Base

class Percepcion(Base):
    """Modelo que representa una percepción de impuesto"""
    
    __tablename__ = 'percepciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_comprobante = Column(String(20))
    numero_documento = Column(String(20))
    proveedor = Column(String(100))
    ruc_proveedor = Column(String(11))
    fecha_emision = Column(Date)  # ← CORREGIDO: antes era 'fecha'
    monto = Column(Float)
    porcentaje = Column(Float)
    monto_percibido = Column(Float)
    mes = Column(Integer)
    anio = Column(Integer)
    ruta_pdf = Column(String(255))
    fecha_subida = Column(DateTime)
    estado = Column(String(20))
    
    def __repr__(self):
        return f"<Percepcion {self.numero_comprobante} - {self.proveedor}>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario para JSON"""
        return {
            'id': self.id,
            'numero_comprobante': self.numero_comprobante,
            'numero_documento': self.numero_documento,
            'proveedor': self.proveedor,
            'ruc_proveedor': self.ruc_proveedor,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'monto': self.monto,
            'porcentaje': self.porcentaje,
            'monto_percibido': self.monto_percibido,
            'mes': self.mes,
            'anio': self.anio,
            'estado': self.estado
        }