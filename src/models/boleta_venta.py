# src/models/boleta_venta.py
from app import db
from datetime import datetime

class BoletaVenta(db.Model):
    __tablename__ = 'boletas_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    fecha_emision = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    cliente = db.Column(db.String(200))
    descripcion = db.Column(db.String(500))
    archivo = db.Column(db.String(200))
    mes = db.Column(db.Integer)
    anio = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BoletaVenta {self.numero}>"