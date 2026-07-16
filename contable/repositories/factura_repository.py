# src/repositories/factura_repository.py
from contable.extensions import db
from sqlalchemy import func
from .base_repository import BaseRepository
from contable.models.factura_compra import FacturaCompra

class FacturaRepository(BaseRepository):
    """Repositorio para FacturaCompra"""
    
    def __init__(self):
        super().__init__(FacturaCompra)
    
    def get_by_mes_anio(self, mes, anio):
        return self.model.query.filter_by(mes=mes, anio=anio).all()
    
    def get_total_by_mes_anio(self, mes, anio):
        result = db.session.query(func.sum(self.model.monto)).filter_by(mes=mes, anio=anio).scalar()
        return result or 0.0
    
    def get_total_general(self):
        result = db.session.query(func.sum(self.model.monto)).scalar()
        return result or 0.0
    
    def upsert(self, numero, **kwargs):
        existing = self.model.query.filter_by(numero=numero).first()
        if existing:
            for key, value in kwargs.items():
                setattr(existing, key, value)
            db.session.commit()
            return existing
        else:
            nueva = self.model(numero=numero, **kwargs)
            db.session.add(nueva)
            db.session.commit()
            return nueva