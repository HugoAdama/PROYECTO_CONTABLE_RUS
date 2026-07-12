"""
Repositorio para operaciones con percepciones
Maneja duplicados automáticamente (UPSERT)
"""
from src.models.percepcion import Percepcion

class PercepcionRepository:
    """Repositorio para la tabla percepciones con manejo de duplicados"""
    
    def __init__(self, session):
        self.session = session
    
    def obtener_por_mes_anio(self, mes, anio):
        """Obtiene percepciones filtradas por mes y año"""
        return self.session.query(Percepcion).filter(
            Percepcion.mes == mes,
            Percepcion.anio == anio
        ).all()
    
    def obtener_todas(self):
        """Obtiene todas las percepciones"""
        return self.session.query(Percepcion).all()
    
    def guardar(self, percepcion):
        """
        Guarda una percepción en la base de datos.
        Si ya existe una percepción con el mismo comprobante, la actualiza.
        """
        try:
            # Verificar si ya existe una percepción con el mismo número
            existente = self.session.query(Percepcion).filter(
                Percepcion.numero_comprobante == percepcion.numero_comprobante
            ).first()
            
            if existente:
                # Actualizar el registro existente
                print(f"🔄 Actualizando percepción existente: {percepcion.numero_comprobante}")
                
                for key, value in percepcion.__dict__.items():
                    if not key.startswith('_'):
                        setattr(existente, key, value)
                
                self.session.commit()
                print(f"✅ Percepción actualizada: {existente.numero_comprobante}")
                return existente
            else:
                # Insertar nueva percepción
                self.session.add(percepcion)
                self.session.commit()
                print(f"✅ Percepción guardada: {percepcion.numero_comprobante}")
                return percepcion
                
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al guardar percepción: {e}")
            raise
    
    def eliminar(self, percepcion_id):
        """Elimina una percepción por ID"""
        try:
            percepcion = self.session.query(Percepcion).filter(
                Percepcion.id == percepcion_id
            ).first()
            if percepcion:
                self.session.delete(percepcion)
                self.session.commit()
                print(f"🗑️ Percepción eliminada: {percepcion.numero_comprobante}")
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al eliminar percepción: {e}")
            raise