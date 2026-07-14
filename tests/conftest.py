"""
Configuración central de pytest para el Sistema de Control Financiero RUS.
"""
import pytest
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion

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
# FACTURAS REALES - NOMBRES EXACTOS
# ============================================

@pytest.fixture
def factura_30022():
    return FacturaCompra(
        fecha_emision=date(2026, 5, 8),
        numero='F033-00330022',          # ✅ campo EXACTO
        monto=750.13,
        proveedor='Natura Cosméticos S.A.'
    )

@pytest.fixture
def factura_30623():
    return FacturaCompra(
        fecha_emision=date(2026, 5, 12),
        numero='F033-00330623',          # ✅ campo EXACTO
        monto=191.70,
        proveedor='Natura Cosméticos S.A.'
    )

@pytest.fixture
def factura_31167():
    return FacturaCompra(
        fecha_emision=date(2026, 5, 14),
        numero='F033-00331167',          # ✅ campo EXACTO
        monto=450.37,
        proveedor='Natura Cosméticos S.A.'
    )

# ============================================
# BOLETAS REALES - NOMBRES EXACTOS
# ============================================

@pytest.fixture
def boleta_302():
    return BoletaVenta(
        fecha_emision=date(2026, 5, 15),
        numero='EB01-302',               # ✅ campo EXACTO
        monto=200.00,
        cliente='DE LA CRUZ MELCHOR MARIA TERESA'
    )

@pytest.fixture
def boleta_303():
    return BoletaVenta(
        fecha_emision=date(2026, 5, 20),
        numero='EB01-303',               # ✅ campo EXACTO
        monto=220.00,
        cliente='DE LA CRUZ MELCHOR MARIA TERESA'
    )

@pytest.fixture
def boleta_304():
    return BoletaVenta(
        fecha_emision=date(2026, 5, 25),
        numero='EB01-304',               # ✅ campo EXACTO
        monto=140.00,
        cliente='DE LA CRUZ MELCHOR MARIA TERESA'
    )

# ============================================
# PERCEPCIÓN REAL - NOMBRES EXACTOS
# ============================================

@pytest.fixture
def percepcion_real():
    return Percepcion(
        fecha_emision=date(2026, 5, 28),
        numero='P003-00602821',          # ✅ campo EXACTO
        monto=441.54,                    # ✅ campo EXACTO
        proveedor='Natura Cosméticos S.A.'
    )

# ============================================
# FIXTURES PARA EXTRACTORES DE PDF
# ============================================

import os
from src.extractors.base_extractor import BaseExtractor
from src.extractors.factura_extractor import FacturaExtractor
from src.extractors.boleta_extractor import BoletaExtractor
from src.extractors.percepcion_extractor import PercepcionExtractor
from src.extractors.detector_extractor import DetectorExtractor

# Ruta a los PDFs reales
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
PDFS_REALES_DIR = os.path.join(FIXTURES_DIR, 'pdfs_reales')


@pytest.fixture
def base_extractor():
    """Fixture para el extractor base."""
    return BaseExtractor()


@pytest.fixture
def factura_extractor():
    """Fixture para el extractor de facturas."""
    return FacturaExtractor()


@pytest.fixture
def boleta_extractor():
    """Fixture para el extractor de boletas."""
    return BoletaExtractor()


@pytest.fixture
def percepcion_extractor():
    """Fixture para el extractor de percepciones."""
    return PercepcionExtractor()


@pytest.fixture
def detector_extractor():
    """Fixture para el detector de tipo de documento."""
    return DetectorExtractor()


# ============================================
# FIXTURES DE RUTAS A PDFS REALES
# ============================================

@pytest.fixture
def ruta_factura_30022():
    """Ruta a la factura F033-00330022."""
    return os.path.join(PDFS_REALES_DIR, '20101796532-01-F033-00330022.pdf')


@pytest.fixture
def ruta_factura_30623():
    """Ruta a la factura F033-00330623."""
    return os.path.join(PDFS_REALES_DIR, '20101796532-01-F033-00330623.pdf')


@pytest.fixture
def ruta_factura_31167():
    """Ruta a la factura F033-00331167."""
    return os.path.join(PDFS_REALES_DIR, '20101796532-01-F033-00331167.pdf')


@pytest.fixture
def ruta_boleta_302():
    """Ruta a la boleta EB01-302."""
    return os.path.join(PDFS_REALES_DIR, 'PDF-BOLETAEB01-30215117337437.pdf')


@pytest.fixture
def ruta_boleta_303():
    """Ruta a la boleta EB01-303."""
    return os.path.join(PDFS_REALES_DIR, 'PDF-BOLETAEB01-30315117337437.pdf')


@pytest.fixture
def ruta_boleta_304():
    """Ruta a la boleta EB01-304."""
    return os.path.join(PDFS_REALES_DIR, 'PDF-BOLETAEB01-30415117337437.pdf')


@pytest.fixture
def ruta_percepcion_real():
    """Ruta a la percepción P003-00602821."""
    return os.path.join(PDFS_REALES_DIR, '20101796532-40-P003-00602821.pdf')
