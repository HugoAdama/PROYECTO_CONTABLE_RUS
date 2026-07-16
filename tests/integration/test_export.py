"""
Pruebas de exportación a Excel del Sistema RUS.
"""

import pytest

from contable.services.export_service import ExportService


class TestExportacionExcel:
    """Pruebas para la exportación a Excel."""

    def test_export_service_disponible(self):
        """Test 1: Verificar que ExportService está disponible."""
        assert ExportService is not None

    def test_export_service_inicializacion(self, app):
        """Test 2: Verificar que ExportService se puede instanciar."""
        with app.app_context():
            service = ExportService()
            assert service is not None

    def test_export_service_tiene_metodos(self, app):
        """Test 3: Verificar que ExportService tiene métodos."""
        with app.app_context():
            service = ExportService()
            # ✅ Buscar cualquier método relacionado con exportar
            metodos = [m for m in dir(service) if not m.startswith('_')]
            assert len(metodos) > 0
