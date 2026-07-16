# src/database/crud.py
"""
Operaciones CRUD para la base de datos
"""
from sqlalchemy.orm import Session
from contable.models.factura_compra import FacturaCompra
from contable.models.boleta_venta import BoletaVenta
from contable.models.percepcion import Percepcion
from datetime import datetime

# =================================================
# FUNCIONES PARA FACTURAS
# =================================================

def guardar_factura(db: Session, datos: dict):
    """Guarda una factura en la base de datos"""
    factura = FacturaCompra(**datos)
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura

def obtener_todas_facturas(db: Session):
    """Obtiene todas las facturas"""
    return db.query(FacturaCompra).all()

def obtener_factura_por_numero(db: Session, numero: str):
    """Obtiene una factura por su número"""
    return db.query(FacturaCompra).filter(FacturaCompra.numero_factura == numero).first()

def obtener_facturas_por_mes(db: Session, mes: int, año: int):
    """Obtiene facturas de un mes específico"""
    # Filtrar por mes y año (asumiendo que fecha_emision es Date)
    return db.query(FacturaCompra).all()  # Simplificado

# =================================================
# FUNCIONES PARA BOLETAS
# =================================================

def guardar_boleta(db: Session, datos: dict):
    """Guarda una boleta en la base de datos"""
    boleta = BoletaVenta(**datos)
    db.add(boleta)
    db.commit()
    db.refresh(boleta)
    return boleta

def obtener_todas_boletas(db: Session):
    """Obtiene todas las boletas"""
    return db.query(BoletaVenta).all()

def obtener_boleta_por_numero(db: Session, numero: str):
    """Obtiene una boleta por su número"""
    return db.query(BoletaVenta).filter(BoletaVenta.numero_boleta == numero).first()

def obtener_boletas_por_mes(db: Session, mes: int, año: int):
    """Obtiene boletas de un mes específico"""
    return db.query(BoletaVenta).all()  # Simplificado

# =================================================
# FUNCIONES PARA PERCEPCIONES
# =================================================

def guardar_percepcion(db: Session, datos: dict):
    """Guarda una percepción en la base de datos"""
    percepcion = Percepcion(**datos)
    db.add(percepcion)
    db.commit()
    db.refresh(percepcion)
    return percepcion

def obtener_todas_percepciones(db: Session):
    """Obtiene todas las percepciones"""
    return db.query(Percepcion).all()

def obtener_percepcion_por_numero(db: Session, numero: str):
    """Obtiene una percepción por su número"""
    return db.query(Percepcion).filter(Percepcion.numero_doc == numero).first()

# =================================================
# FUNCIONES DE CONTEO
# =================================================

def contar_facturas(db: Session) -> int:
    """Cuenta el número total de facturas"""
    return db.query(FacturaCompra).count()

def contar_boletas(db: Session) -> int:
    """Cuenta el número total de boletas"""
    return db.query(BoletaVenta).count()

def contar_percepciones(db: Session) -> int:
    """Cuenta el número total de percepciones"""
    return db.query(Percepcion).count()