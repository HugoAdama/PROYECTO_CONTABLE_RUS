# src/database/models.py
# ======================
# Modelos de base de datos para el Sistema RUS
# ======================

from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Boolean, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from src.database.conexion import db


class Documento(db.Model):
    """
    Modelo ÚNICO para todos los tipos de documentos.
    Tipos soportados: factura, boleta, percepcion
    """
    __tablename__ = 'documentos'
    
    id = Column(Integer, primary_key=True)
    
    # === IDENTIFICACIÓN ===
    numero = Column(String(50), nullable=False, index=True)
    tipo = Column(String(20), nullable=False, index=True)
    ruc_emisor = Column(String(11), index=True)
    ruc_cliente = Column(String(11), index=True)
    
    # === DATOS PRINCIPALES ===
    nombre_cliente = Column(String(200))
    fecha_emision = Column(Date, nullable=False, index=True)
    moneda = Column(String(3), default='PEN')
    ciclo = Column(String(10))
    
    # === MONTOS (DECIMAL para precisión) ===
    monto_total = Column(Numeric(12, 2), nullable=False)
    monto_base = Column(Numeric(12, 2), default=0.00)
    percepcion = Column(Numeric(12, 2), default=0.00)
    
    # === METADATOS ===
    archivo_original = Column(String(200))
    fecha_procesamiento = Column(DateTime, default=datetime.utcnow)
    
    # === PARA PERCEPCIONES ===
    documento_asociado = Column(String(50))
    mes_aplicacion = Column(String(10))
    
    # === ÍNDICES COMPUESTOS ===
    __table_args__ = (
        Index('idx_documento_fecha_tipo', 'fecha_emision', 'tipo'),
        Index('idx_documento_ruc_fecha', 'ruc_cliente', 'fecha_emision'),
    )
    
    def __repr__(self):
        return f"<Documento {self.tipo}: {self.numero} - S/{self.monto_total:.2f}>"
    
    def to_dict(self):
        """Convierte a diccionario para JSON"""
        return {
            'id': self.id,
            'numero': self.numero,
            'tipo': self.tipo,
            'ruc_emisor': self.ruc_emisor,
            'ruc_cliente': self.ruc_cliente,
            'nombre_cliente': self.nombre_cliente,
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'monto_total': float(self.monto_total),
            'monto_base': float(self.monto_base),
            'percepcion': float(self.percepcion),
            'archivo_original': self.archivo_original,
            'documento_asociado': self.documento_asociado,
            'ciclo': self.ciclo,
            'fecha_procesamiento': self.fecha_procesamiento.isoformat()
        }


class Configuracion(db.Model):
    """
    Configuración del sistema (persistente en BD)
    """
    __tablename__ = 'configuracion'
    
    id = Column(Integer, primary_key=True)
    clave = Column(String(50), unique=True, nullable=False)
    valor = Column(Text, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Configuracion {self.clave}={self.valor}>"
    
    @staticmethod
    def get(clave, default=None):
        """Obtiene un valor de configuración"""
        from src.database.conexion import db
        config = Configuracion.query.filter_by(clave=clave).first()
        return config.valor if config else default
    
    @staticmethod
    def set(clave, valor):
        """Establece un valor de configuración"""
        from src.database.conexion import db
        config = Configuracion.query.filter_by(clave=clave).first()
        if config:
            config.valor = valor
        else:
            config = Configuracion(clave=clave, valor=valor)
            db.session.add(config)
        db.session.commit()


class Historial(db.Model):
    """
    Historial de acciones del usuario
    """
    __tablename__ = 'historial'
    
    id = Column(Integer, primary_key=True)
    accion = Column(String(50), nullable=False)
    detalle = Column(Text)
    usuario = Column(String(100), default='Doña María')
    fecha = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<Historial {self.accion} - {self.fecha}>"
    
    @staticmethod
    def registrar(accion, detalle=None, usuario='Doña María'):
        """Registra una acción en el historial"""
        from src.database.conexion import db
        entry = Historial(accion=accion, detalle=detalle, usuario=usuario)
        db.session.add(entry)
        db.session.commit()
        return entry
