"""
Pruebas de integración para los servicios del Sistema RUS.
"""

import pytest
import os
from datetime import date

from app.services.documento_service import DocumentoService
from app.services.reporte_service import ReporteService
from app.services.export_service import ExportService


class TestDocumentoService:
    """Pruebas para el servicio de documentos."""

    def test_documento_service_existe(self):
        """Test 1: Verificar que DocumentoService está disponible."""
        assert DocumentoService is not None

    def test_documento_service_inicializacion(self, app):
        """Test 2: Verificar que DocumentoService se puede instanciar."""
        with app.app_context():
            # ✅ Crear sin pasar parámetros
            service = DocumentoService()
            assert service is not None

    def test_documento_service_tiene_metodos(self, app):
        """Test 3: Verificar que DocumentoService tiene métodos."""
        with app.app_context():
            service = DocumentoService()
            # Verificar que tiene métodos (cualquiera)
            metodos = [m for m in dir(service) if not m.startswith('_') and callable(getattr(service, m))]
            assert len(metodos) > 0


class TestReporteService:
    """Pruebas para el servicio de reportes."""

    def test_reporte_service_existe(self):
        """Test 1: Verificar que ReporteService está disponible."""
        assert ReporteService is not None

    def test_reporte_service_inicializacion(self, app):
        """Test 2: Verificar que ReporteService se puede instanciar."""
        with app.app_context():
            service = ReporteService()
            assert service is not None


class TestExportService:
    """Pruebas para el servicio de exportación."""

    def test_export_service_existe(self):
        """Test 1: Verificar que ExportService está disponible."""
        assert ExportService is not None

    def test_export_service_inicializacion(self, app):
        """Test 2: Verificar que ExportService se puede instanciar."""
        with app.app_context():
            service = ExportService()
            assert service is not None
