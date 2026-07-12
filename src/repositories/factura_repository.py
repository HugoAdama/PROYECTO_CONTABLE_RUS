"""
Repositorio para operaciones con facturas de compra
Maneja duplicados automáticamente (UPSERT)
"""
from src.models.factura_compra import FacturaCompra

class FacturaRepository:
    """Repositorio para la tabla facturas_compras con manejo de duplicados"""
    
    def __init__(self, session):
        self.session = session
    
    def obtener_por_mes_anio(self, mes, anio):
        """Obtiene facturas filtradas por mes y año"""
        return self.session.query(FacturaCompra).filter(
            FacturaCompra.mes == mes,
            FacturaCompra.anio == anio
        ).all()
    
    def obtener_todas(self):
        """Obtiene todas las facturas"""
        return self.session.query(FacturaCompra).all()
    
    def guardar(self, factura):
        """
        Guarda una factura en la base de datos.
        Si ya existe una factura con el mismo número, la actualiza.
        """
        try:
            # Verificar si ya existe una factura con el mismo número
            existente = self.session.query(FacturaCompra).filter(
                FacturaCompra.numero_factura == factura.numero_factura
            ).first()
            
            if existente:
                # Actualizar el registro existente
                print(f"🔄 Actualizando factura existente: {factura.numero_factura}")
                
                for key, value in factura.__dict__.items():
                    if not key.startswith('_'):
                        setattr(existente, key, value)
                
                self.session.commit()
                print(f"✅ Factura actualizada: {existente.numero_factura}")
                return existente
            else:
                # Insertar nueva factura
                self.session.add(factura)
                self.session.commit()
                print(f"✅ Factura guardada: {factura.numero_factura}")
                return factura
                
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al guardar factura: {e}")
            raise
    
    def eliminar(self, factura_id):
        """Elimina una factura por ID"""
        try:
            factura = self.session.query(FacturaCompra).filter(
                FacturaCompra.id == factura_id
            ).first()
            if factura:
                self.session.delete(factura)
                self.session.commit()
                print(f"🗑️ Factura eliminada: {factura.numero_factura}")
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al eliminar factura: {e}")
            raise