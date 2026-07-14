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
