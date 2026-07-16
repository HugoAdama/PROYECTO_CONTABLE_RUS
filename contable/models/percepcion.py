# src/models/percepcion.py
from contable.extensions import db
from datetime import datetime, timezone

class Percepcion(db.Model):
    __tablename__ = 'percepciones'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    fecha_emision = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    proveedor = db.Column(db.String(200))
    descripcion = db.Column(db.String(500))
    archivo = db.Column(db.String(200))
    mes = db.Column(db.Integer)
    anio = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Percepcion {self.numero}>"
