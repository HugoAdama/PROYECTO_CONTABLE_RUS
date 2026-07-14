"""
Pruebas unitarias para los repositorios del Sistema RUS.
"""

import pytest
from datetime import date

from src.repositories.factura_repository import FacturaRepository
from src.repositories.boleta_repository import BoletaRepository
from src.repositories.percepcion_repository import PercepcionRepository
from src.models.factura_compra import FacturaCompra
from src.models.boleta_venta import BoletaVenta
from src.models.percepcion import Percepcion


# ============================================
# PRUEBAS DE FACTURA REPOSITORY
# ============================================

class TestFacturaRepository:
    """Pruebas para el repositorio de facturas."""

    def test_upsert_factura(self, app):
        """Test 1: Crear/Actualizar una factura usando upsert."""
        with app.app_context():
            FacturaCompra.query.delete()
            
            repo = FacturaRepository()
            
            factura_guardada = repo.upsert(
                numero='F033-00330623',
                fecha_emision=date(2026, 5, 12),
                monto=191.70,
                proveedor='NATURA COSMETICOS S.A.',
                mes=5,
                anio=2026
            )
            
            assert factura_guardada is not None
            assert factura_guardada.numero == 'F033-00330623'
            assert factura_guardada.monto == 191.70

    def test_get_total_general_facturas(self, app):
        """Test 2: Obtener total general de facturas."""
        with app.app_context():
            FacturaCompra.query.delete()
            
            repo = FacturaRepository()
            
            repo.upsert(numero='F033-00330022', fecha_emision=date(2026, 5, 8), monto=750.13, proveedor='NATURA', mes=5, anio=2026)
            repo.upsert(numero='F033-00330623', fecha_emision=date(2026, 5, 12), monto=191.70, proveedor='NATURA', mes=5, anio=2026)
            repo.upsert(numero='F033-00331167', fecha_emision=date(2026, 5, 14), monto=450.37, proveedor='NATURA', mes=5, anio=2026)
            
            total = repo.get_total_general()
            assert total == pytest.approx(1392.20, 0.01)

    def test_get_total_by_mes_anio_facturas(self, app):
        """Test 3: Obtener total de facturas por mes y año."""
        with app.app_context():
            FacturaCompra.query.delete()
            
            repo = FacturaRepository()
            
            repo.upsert(numero='F033-00330022', fecha_emision=date(2026, 5, 8), monto=750.13, proveedor='NATURA', mes=5, anio=2026)
            repo.upsert(numero='F033-00330623', fecha_emision=date(2026, 5, 12), monto=191.70, proveedor='NATURA', mes=5, anio=2026)
            repo.upsert(numero='F033-00339999', fecha_emision=date(2026, 6, 1), monto=500.00, proveedor='OTRO', mes=6, anio=2026)
            
            total_mayo = repo.get_total_by_mes_anio(mes=5, anio=2026)
            # ✅ Usar approx para flotantes
            assert total_mayo == pytest.approx(941.83, 0.01)

    def test_get_by_mes_anio_facturas(self, app):
        """Test 4: Obtener facturas por mes y año."""
        with app.app_context():
            FacturaCompra.query.delete()
            
            repo = FacturaRepository()
            
            repo.upsert(numero='F033-00330022', fecha_emision=date(2026, 5, 8), monto=750.13, proveedor='NATURA', mes=5, anio=2026)
            repo.upsert(numero='F033-00330623', fecha_emision=date(2026, 5, 12), monto=191.70, proveedor='NATURA', mes=5, anio=2026)
            
            facturas = repo.get_by_mes_anio(mes=5, anio=2026)
            
            assert len(facturas) >= 2
            assert any(f.numero == 'F033-00330022' for f in facturas)
            assert any(f.numero == 'F033-00330623' for f in facturas)


# ============================================
# PRUEBAS DE BOLETA REPOSITORY
# ============================================

class TestBoletaRepository:
    """Pruebas para el repositorio de boletas."""

    def test_upsert_boleta(self, app):
        """Test 1: Crear/Actualizar una boleta usando upsert."""
        with app.app_context():
            BoletaVenta.query.delete()
            
            repo = BoletaRepository()
            
            boleta_guardada = repo.upsert(
                numero='EB01-302',
                fecha_emision=date(2026, 5, 31),
                monto=200.00,
                cliente='KAROLAY CHAVEZ',
                mes=5,
                anio=2026
            )
            
            assert boleta_guardada is not None
            assert boleta_guardada.numero == 'EB01-302'
            assert boleta_guardada.monto == 200.00

    def test_get_total_general_boletas(self, app):
        """Test 2: Obtener total general de boletas."""
        with app.app_context():
            BoletaVenta.query.delete()
            
            repo = BoletaRepository()
            
            repo.upsert(numero='EB01-302', fecha_emision=date(2026, 5, 31), monto=200.00, cliente='KAROLAY', mes=5, anio=2026)
            repo.upsert(numero='EB01-303', fecha_emision=date(2026, 5, 31), monto=220.00, cliente='INACIA', mes=5, anio=2026)
            repo.upsert(numero='EB01-304', fecha_emision=date(2026, 5, 31), monto=140.00, cliente='BEICY', mes=5, anio=2026)
            
            total = repo.get_total_general()
            assert total == 560.00

    def test_get_total_by_mes_anio_boletas(self, app):
        """Test 3: Obtener total de boletas por mes y año."""
        with app.app_context():
            BoletaVenta.query.delete()
            
            repo = BoletaRepository()
            
            repo.upsert(numero='EB01-302', fecha_emision=date(2026, 5, 31), monto=200.00, cliente='KAROLAY', mes=5, anio=2026)
            repo.upsert(numero='EB01-303', fecha_emision=date(2026, 6, 1), monto=220.00, cliente='INACIA', mes=6, anio=2026)
            
            total_mayo = repo.get_total_by_mes_anio(mes=5, anio=2026)
            total_junio = repo.get_total_by_mes_anio(mes=6, anio=2026)
            
            assert total_mayo == 200.00
            assert total_junio == 220.00

    def test_get_by_mes_anio_boletas(self, app):
        """Test 4: Obtener boletas por mes y año."""
        with app.app_context():
            BoletaVenta.query.delete()
            
            repo = BoletaRepository()
            
            repo.upsert(numero='EB01-302', fecha_emision=date(2026, 5, 31), monto=200.00, cliente='KAROLAY', mes=5, anio=2026)
            repo.upsert(numero='EB01-303', fecha_emision=date(2026, 5, 31), monto=220.00, cliente='INACIA', mes=5, anio=2026)
            
            boletas = repo.get_by_mes_anio(mes=5, anio=2026)
            
            assert len(boletas) >= 2


# ============================================
# PRUEBAS DE PERCEPCION REPOSITORY
# ============================================

class TestPercepcionRepository:
    """Pruebas para el repositorio de percepciones."""

    def test_upsert_percepcion(self, app):
        """Test 1: Crear/Actualizar una percepción usando upsert."""
        with app.app_context():
            Percepcion.query.delete()
            
            repo = PercepcionRepository()
            
            percepcion_guardada = repo.upsert(
                numero='P003-00602821',
                fecha_emision=date(2026, 7, 14),
                monto=441.54,
                proveedor='NATURA COSMETICOS S.A.',
                mes=7,
                anio=2026
            )
            
            assert percepcion_guardada is not None
            assert percepcion_guardada.numero == 'P003-00602821'
            assert percepcion_guardada.monto == 441.54

    def test_get_total_general_percepciones(self, app):
        """Test 2: Obtener total general de percepciones."""
        with app.app_context():
            Percepcion.query.delete()
            
            repo = PercepcionRepository()
            
            repo.upsert(numero='P003-00602821', fecha_emision=date(2026, 7, 14), monto=441.54, proveedor='NATURA', mes=7, anio=2026)
            
            total = repo.get_total_general()
            assert total == 441.54


# ============================================
# PRUEBAS DE INTEGRACIÓN
# ============================================

class TestRepositoriosIntegracion:
    """Pruebas de integración entre repositorios."""

    def test_todos_los_repositorios_funcionan(self, app):
        """Test 1: Todos los repositorios funcionan correctamente."""
        with app.app_context():
            FacturaCompra.query.delete()
            BoletaVenta.query.delete()
            Percepcion.query.delete()
            
            factura_repo = FacturaRepository()
            boleta_repo = BoletaRepository()
            percepcion_repo = PercepcionRepository()
            
            f = factura_repo.upsert(numero='F033-00330623', fecha_emision=date(2026, 5, 12), monto=191.70, proveedor='NATURA', mes=5, anio=2026)
            b = boleta_repo.upsert(numero='EB01-302', fecha_emision=date(2026, 5, 31), monto=200.00, cliente='KAROLAY', mes=5, anio=2026)
            p = percepcion_repo.upsert(numero='P003-00602821', fecha_emision=date(2026, 7, 14), monto=441.54, proveedor='NATURA', mes=7, anio=2026)
            
            assert f is not None
            assert b is not None
            assert p is not None
            
            assert factura_repo.get_total_general() == pytest.approx(191.70, 0.01)
            assert boleta_repo.get_total_general() == 200.00
            assert percepcion_repo.get_total_general() == 441.54
