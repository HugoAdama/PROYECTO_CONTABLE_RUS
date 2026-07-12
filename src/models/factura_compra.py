"""
Modelo SQLAlchemy para la tabla facturas_compras
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from src.database.conexion import Base

class FacturaCompra(Base):
    """Modelo que representa una factura de compra"""
    
    __tablename__ = 'facturas_compras'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc_proveedor = Column(String(11))
    proveedor = Column(String(100))
    direccion_proveedor = Column(String(200))
    telefono_proveedor = Column(String(20))
    numero_factura = Column(String(20))
    fecha_emision = Column(Date)  # ← CORREGIDO: antes era 'fecha'
    fecha_vencimiento = Column(Date)
    tipo_comprobante = Column(String(20))
    serie = Column(String(10))
    sub_total = Column(Float)
    igv = Column(Float)
    total_con_descuento = Column(Float)
    percepcion = Column(Float)
    total_pagar = Column(Float)
    otros_cargos = Column(Float)
    descuento = Column(Float)
    productos = Column(Text)
    cantidad_productos = Column(Integer)
    mes = Column(Integer)
    anio = Column(Integer)
    ruta_pdf = Column(String(255))
    fecha_subida = Column(DateTime)
    estado = Column(String(20))
    observaciones = Column(Text)
    
    def __repr__(self):
        return f"<FacturaCompra {self.numero_factura} - {self.proveedor}>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario para JSON"""
        return {
            'id': self.id,
            'ruc_proveedor': self.ruc_proveedor,
            'proveedor': self.proveedor,
            'direccion_proveedor': self.direccion_proveedor,
            'telefono_proveedor': self.telefono_proveedor,
            'numero_factura': self.numero_factura,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'tipo_comprobante': self.tipo_comprobante,
            'serie': self.serie,
            'sub_total': self.sub_total,
            'igv': self.igv,
            'total_con_descuento': self.total_con_descuento,
            'percepcion': self.percepcion,
            'total_pagar': self.total_pagar,
            'otros_cargos': self.otros_cargos,
            'descuento': self.descuento,
            'productos': self.productos,
            'cantidad_productos': self.cantidad_productos,
            'mes': self.mes,
            'anio': self.anio,
            'estado': self.estado,
            'observaciones': self.observaciones
        }