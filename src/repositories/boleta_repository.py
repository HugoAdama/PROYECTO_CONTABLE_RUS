"""
Repositorio para operaciones con boletas de venta
Maneja duplicados automáticamente (UPSERT)
"""
from src.models.boleta_venta import BoletaVenta

class BoletaRepository:
    """Repositorio para la tabla boletas_venta con manejo de duplicados"""
    
    def __init__(self, session):
        self.session = session
    
    def obtener_por_mes_anio(self, mes, anio):
        """Obtiene boletas filtradas por mes y año"""
        return self.session.query(BoletaVenta).filter(
            BoletaVenta.mes == mes,
            BoletaVenta.anio == anio
        ).all()
    
    def obtener_todas(self):
        """Obtiene todas las boletas"""
        return self.session.query(BoletaVenta).all()
    
    def guardar(self, boleta):
        """
        Guarda una boleta en la base de datos.
        Si ya existe una boleta con el mismo número, la actualiza.
        Esto evita errores de duplicados para usuarios que suben el mismo archivo varias veces.
        """
        try:
            # Verificar si ya existe una boleta con el mismo número
            existente = self.session.query(BoletaVenta).filter(
                BoletaVenta.numero_boleta == boleta.numero_boleta
            ).first()
            
            if existente:
                # Actualizar el registro existente con los nuevos datos
                print(f"🔄 Actualizando boleta existente: {boleta.numero_boleta}")
                
                # Copiar todos los atributos del nuevo objeto al existente
                for key, value in boleta.__dict__.items():
                    if not key.startswith('_'):  # Ignorar atributos internos de SQLAlchemy
                        setattr(existente, key, value)
                
                self.session.commit()
                print(f"✅ Boleta actualizada: {existente.numero_boleta}")
                return existente
            else:
                # Insertar nueva boleta
                self.session.add(boleta)
                self.session.commit()
                print(f"✅ Boleta guardada: {boleta.numero_boleta}")
                return boleta
                
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al guardar boleta: {e}")
            raise
    
    def eliminar(self, boleta_id):
        """Elimina una boleta por ID"""
        try:
            boleta = self.session.query(BoletaVenta).filter(
                BoletaVenta.id == boleta_id
            ).first()
            if boleta:
                self.session.delete(boleta)
                self.session.commit()
                print(f"🗑️ Boleta eliminada: {boleta.numero_boleta}")
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al eliminar boleta: {e}")
            raise