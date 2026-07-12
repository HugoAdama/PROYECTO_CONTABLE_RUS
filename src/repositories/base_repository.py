# src/repositories/base_repository.py
"""
📁 REPOSITORIO BASE
Define las operaciones CRUD genéricas para todas las entidades
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Type
from sqlalchemy.orm import Session
from src.database.conexion import SessionLocal

T = TypeVar('T')  # Tipo genérico para las entidades

class BaseRepository(ABC, Generic[T]):
    """
    Repositorio base con operaciones CRUD genéricas.
    Todas las entidades heredan de esta clase.
    """
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self.db = SessionLocal()
    
    def guardar(self, datos: dict) -> T:
        """
        Guarda una nueva entidad en la base de datos.
        """
        try:
            entidad = self.model_class(**datos)
            self.db.add(entidad)
            self.db.commit()
            self.db.refresh(entidad)
            return entidad
        except Exception as e:
            self.db.rollback()
            raise e
    
    def obtener_por_id(self, id: int) -> Optional[T]:
        """
        Obtiene una entidad por su ID.
        """
        return self.db.query(self.model_class).filter(
            self.model_class.id == id
        ).first()
    
    def obtener_todos(self) -> List[T]:
        """
        Obtiene todas las entidades.
        """
        return self.db.query(self.model_class).all()
    
    def actualizar(self, id: int, datos: dict) -> Optional[T]:
        """
        Actualiza una entidad existente.
        """
        try:
            entidad = self.obtener_por_id(id)
            if not entidad:
                return None
            
            for clave, valor in datos.items():
                if hasattr(entidad, clave):
                    setattr(entidad, clave, valor)
            
            self.db.commit()
            self.db.refresh(entidad)
            return entidad
        except Exception as e:
            self.db.rollback()
            raise e
    
    def eliminar(self, id: int) -> bool:
        """
        Elimina una entidad por su ID.
        """
        try:
            entidad = self.obtener_por_id(id)
            if not entidad:
                return False
            
            self.db.delete(entidad)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e
    
    def contar(self) -> int:
        """
        Cuenta el número total de entidades.
        """
        return self.db.query(self.model_class).count()
    
    def close(self):
        """
        Cierra la sesión de la base de datos.
        """
        self.db.close()