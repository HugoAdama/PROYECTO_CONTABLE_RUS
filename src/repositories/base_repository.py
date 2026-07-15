# src/repositories/base_repository.py
from app import db

class BaseRepository:
    """Repositorio base con operaciones CRUD genéricas"""
    
    def __init__(self, model):
        self.model = model
    
    def get_all(self):
        """Obtiene todos los registros"""
        return self.model.query.all()
    
    def get_by_id(self, id):
        """Obtiene un registro por ID"""
        return self.model.query.get(id)
    
    def create(self, **kwargs):
        """Crea un nuevo registro"""
        obj = self.model(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj
    
    def update(self, id, **kwargs):
        """Actualiza un registro existente"""
        obj = self.get_by_id(id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj
    
    def delete(self, id):
        """Elimina un registro"""
        obj = self.get_by_id(id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    def count(self):
        """Cuenta el número de registros"""
        return self.model.query.count()