# src/repositories/base_repository.py
from typing import List, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime
from src.database.conexion import get_db

class BaseRepository:
    def __init__(self, model_class, session: Session = None):
        self.model_class = model_class
        self.session = session or get_db()

    def crear(self, **kwargs) -> Any:
        try:
            if 'fecha_emision' in kwargs and 'mes' not in kwargs:
                fecha = kwargs['fecha_emision']
                kwargs['mes'] = fecha.month
                kwargs['anio'] = fecha.year
            instancia = self.model_class(**kwargs)
            self.session.add(instancia)
            self.session.commit()
            return instancia
        except Exception as e:
            self.session.rollback()
            raise e

    def obtener_por_id(self, id: int) -> Optional[Any]:
        return self.session.query(self.model_class).filter_by(id=id).first()

    def obtener_todos(self) -> List[Any]:
        return self.session.query(self.model_class).all()

    def obtener_por_mes_anio(self, mes: int, anio: int) -> List[Any]:
        return self.session.query(self.model_class).filter_by(mes=mes, anio=anio).all()

    def actualizar(self, id: int, **kwargs) -> Optional[Any]:
        instancia = self.obtener_por_id(id)
        if instancia:
            for key, value in kwargs.items():
                if hasattr(instancia, key):
                    setattr(instancia, key, value)
            self.session.commit()
        return instancia

    def eliminar(self, id: int) -> bool:
        instancia = self.obtener_por_id(id)
        if instancia:
            self.session.delete(instancia)
            self.session.commit()
            return True
        return False

    def contar(self) -> int:
        return self.session.query(self.model_class).count()

    def close(self):
        if self.session:
            self.session.close()