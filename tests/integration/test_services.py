"""
Pruebas de integración para los servicios del Sistema RUS.
"""

import pytest
import os
from datetime import date
from pathlib import Path

from contable.services.documento_service import DocumentoService
from contable.services.reporte_service import ReporteService
from contable.services.export_service import ExportService


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

    def test_normaliza_factura_extraida(self, app):
        """El orquestador adapta la salida del extractor al modelo unificado."""
        with app.app_context():
            service = DocumentoService()
            datos = service._normalizar(
                "factura",
                {
                    "numero_factura": "F001-123",
                    "fecha_emision": "2026-05-08",
                    "total_pagar": 100.50,
                    "sub_total": 85.17,
                    "igv": 15.33,
                    "proveedor": "Proveedor Demo",
                    "ruc_proveedor": "20123456789",
                },
                Path("factura.pdf"),
            )
            assert datos["tipo"] == "factura"
            assert datos["numero"] == "F001-123"
            assert datos["monto_total"] == 100.50
            assert datos["archivo_original"] == "factura.pdf"

    def test_rechaza_tipo_desconocido(self, app, tmp_path):
        """El flujo no persiste documentos cuyo tipo no puede determinarse."""
        with app.app_context():
            service = DocumentoService()
            service.detector.extraer = lambda _: {"tipo_detectado": "desconocido"}
            resultado = service.procesar_archivo(tmp_path / "desconocido.pdf")
            assert resultado["success"] is False
            assert "tipo" in resultado["message"].lower()


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
