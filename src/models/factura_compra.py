# src/models/factura_compra.py
from app import db
from datetime import datetime, timezone

class FacturaCompra(db.Model):
    __tablename__ = 'facturas_compras'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    fecha_emision = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    impuesto = db.Column(db.Float, default=0.0)
    proveedor = db.Column(db.String(200))
    descripcion = db.Column(db.String(500))
    archivo = db.Column(db.String(200))
    mes = db.Column(db.Integer)
    anio = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<FacturaCompra {self.numero}>"
