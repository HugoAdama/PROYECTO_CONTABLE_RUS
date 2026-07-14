"""
Configuración central de pytest para el Sistema de Control Financiero RUS.
"""
import pytest
import os
import sys
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion

Base = declarative_base()

# ============================================
# FIXTURES DE APLICACIÓN
# ============================================

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# ============================================
# FIXTURE PARA SESIÓN DE BASE DE DATOS
# ============================================

@pytest.fixture
def db_session():
    """Fixture que proporciona una sesión de base de datos para pruebas."""
    engine = create_engine('sqlite:///:memory:')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# FIXTURES CON DATOS REALES DE DOÑA MARÍA
# ============================================

@pytest.fixture
def factura_30022():
    """Factura F033-00330022 - S/ 750.13"""
    return FacturaCompra(
        fecha_emision=date(2026, 5, 8),
        numero='F033-00330022',
        monto=750.13,
        proveedor='NATURA COSMETICOS S.A.'
    )

@pytest.fixture
def factura_30623():
    """Factura F033-00330623 - S/ 191.70"""
    return FacturaCompra(
        fecha_emision=date(2026, 5, 12),
        numero='F033-00330623',
        monto=191.70,
        proveedor='NATURA COSMETICOS S.A.'
    )

@pytest.fixture
def factura_31167():
    """Factura F033-00331167 - S/ 450.37"""
    return FacturaCompra(
        fecha_emision=date(2026, 5, 14),
        numero='F033-00331167',
        monto=450.37,
        proveedor='NATURA COSMETICOS S.A.'
    )

@pytest.fixture
def boleta_302():
    """Boleta EB01-302 - S/ 200.00"""
    return BoletaVenta(
        fecha_emision=date(2026, 5, 31),
        numero='EB01-302',
        monto=200.00,
        cliente='KAROLAY CHAVEZ'
    )

@pytest.fixture
def boleta_303():
    """Boleta EB01-303 - S/ 220.00"""
    return BoletaVenta(
        fecha_emision=date(2026, 5, 31),
        numero='EB01-303',
        monto=220.00,
        cliente='INACIA CHU'
    )

@pytest.fixture
def boleta_304():
    """Boleta EB01-304 - S/ 140.00"""
    return BoletaVenta(
        fecha_emision=date(2026, 5, 31),
        numero='EB01-304',
        monto=140.00,
        cliente='BEICY VAR'
    )

@pytest.fixture
def percepcion_real():
    """Percepción P003-00602821"""
    return Percepcion(
        fecha_emision=date(2026, 7, 14),
        numero='P003-00602821',
        monto=441.54,
        proveedor='NATURA COSMETICOS S.A.'
        # tasa eliminado - no existe en el modelo
    )

# ============================================
# FIXTURES DE RUTAS A PDFS REALES
# ============================================

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
PDFS_REALES_DIR = os.path.join(FIXTURES_DIR, 'pdfs_reales')

@pytest.fixture
def ruta_factura_30623():
    return os.path.join(PDFS_REALES_DIR, '20101796532-01-F033-00330623.pdf')

@pytest.fixture
def ruta_factura_30022():
    return os.path.join(PDFS_REALES_DIR, '20101796532-01-F033-00330022.pdf')

@pytest.fixture
def ruta_factura_31167():
    return os.path.join(PDFS_REALES_DIR, '20101796532-01-F033-00331167.pdf')

@pytest.fixture
def ruta_boleta_302():
    return os.path.join(PDFS_REALES_DIR, 'PDF-BOLETAEB01-30215117337437.pdf')

@pytest.fixture
def ruta_boleta_303():
    return os.path.join(PDFS_REALES_DIR, 'PDF-BOLETAEB01-30315117337437.pdf')

@pytest.fixture
def ruta_boleta_304():
    return os.path.join(PDFS_REALES_DIR, 'PDF-BOLETAEB01-30415117337437.pdf')

@pytest.fixture
def ruta_percepcion_real():
    return os.path.join(PDFS_REALES_DIR, '20101796532-40-P003-00602821.pdf')

# ============================================
# FIXTURES PARA EXTRACTORES
# ============================================

from src.extractors.base_extractor import BaseExtractor
from src.extractors.factura_extractor import FacturaExtractor
from src.extractors.boleta_extractor import BoletaExtractor
from src.extractors.percepcion_extractor import PercepcionExtractor
from src.extractors.detector_extractor import DetectorExtractor

@pytest.fixture
def base_extractor():
    return BaseExtractor()

@pytest.fixture
def factura_extractor():
    return FacturaExtractor()

@pytest.fixture
def boleta_extractor():
    return BoletaExtractor()

@pytest.fixture
def percepcion_extractor():
    return PercepcionExtractor()

@pytest.fixture
def detector_extractor():
    return DetectorExtractor()
