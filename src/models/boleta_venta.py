"""
Modelo SQLAlchemy para la tabla boletas_venta
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from src.database.conexion import Base

class BoletaVenta(Base):
    """Modelo que representa una boleta de venta"""
    
    __tablename__ = 'boletas_venta'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc_cliente = Column(String(11))
    cliente = Column(String(100))
    direccion_cliente = Column(String(200))
    numero_boleta = Column(String(20))
    fecha_emision = Column(Date)  # ← CORREGIDO: antes era 'fecha'
    tipo_comprobante = Column(String(20))
    serie = Column(String(10))
    sub_total = Column(Float)
    igv = Column(Float)
    total_con_descuento = Column(Float)
    total_pagar = Column(Float)
    descuento = Column(Float)
    productos = Column(Text)
    cantidad_productos = Column(Integer)
    mes = Column(Integer)
    anio = Column(Integer)
    ruta_pdf = Column(String(255))
    fecha_subida = Column(DateTime)
    estado = Column(String(20))
    
    def __repr__(self):
        return f"<BoletaVenta {self.numero_boleta} - {self.cliente}>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario para JSON"""
        return {
            'id': self.id,
            'ruc_cliente': self.ruc_cliente,
            'cliente': self.cliente,
            'direccion_cliente': self.direccion_cliente,
            'numero_boleta': self.numero_boleta,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'tipo_comprobante': self.tipo_comprobante,
            'serie': self.serie,
            'sub_total': self.sub_total,
            'igv': self.igv,
            'total_con_descuento': self.total_con_descuento,
            'total_pagar': self.total_pagar,
            'descuento': self.descuento,
            'productos': self.productos,
            'cantidad_productos': self.cantidad_productos,
            'mes': self.mes,
            'anio': self.anio,
            'estado': self.estado
        }