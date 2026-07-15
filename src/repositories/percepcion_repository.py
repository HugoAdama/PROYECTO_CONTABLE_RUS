# src/repositories/percepcion_repository.py
from app import db
from sqlalchemy import func
from .base_repository import BaseRepository
from src.models.percepcion import Percepcion

class PercepcionRepository(BaseRepository):
    """Repositorio para Percepcion"""
    
    def __init__(self):
        super().__init__(Percepcion)
    
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