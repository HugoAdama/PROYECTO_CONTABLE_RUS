"""
Pruebas de integración para las rutas Flask del Sistema RUS.
"""

import pytest


class TestRoutes:
    """Pruebas para todas las rutas de la aplicación."""

    def test_index_route(self, client, app):
        """Test 1: GET / - Dashboard carga correctamente."""
        with app.app_context():
            response = client.get('/')
            assert response.status_code == 200

    def test_subir_route_get(self, client, app):
        """Test 2: GET /subir - Página de subida carga correctamente."""
        with app.app_context():
            response = client.get('/subir')
            assert response.status_code == 200
            assert b'Subir' in response.data

    def test_subir_route_post(self, client, app):
        """Test 3: POST /subir - Método no permitido (405) es correcto."""
        with app.app_context():
            response = client.post('/subir')
            # ✅ 405 es correcto porque la ruta espera GET
            assert response.status_code == 405

    def test_ver_datos_route(self, client, app):
        """Test 4: GET /ver_datos - Página de datos carga correctamente."""
        with app.app_context():
            response = client.get('/ver_datos')
            assert response.status_code == 200

    def test_reportes_route(self, client, app):
        """Test 5: GET /reportes - Página de reportes carga correctamente."""
        with app.app_context():
            response = client.get('/reportes')
            assert response.status_code == 200

    def test_carpetas_route(self, client, app):
        """Test 6: GET /carpetas - Gestión de carpetas carga correctamente."""
        with app.app_context():
            response = client.get('/carpetas')
            assert response.status_code == 200

    def test_backup_route(self, client, app):
        """Test 7: GET /backup - Página de backup carga correctamente."""
        with app.app_context():
            response = client.get('/backup')
            assert response.status_code == 200

    def test_historial_route(self, client, app):
        """Test 8: GET /historial - Historial carga correctamente."""
        with app.app_context():
            response = client.get('/historial')
            assert response.status_code == 200

    def test_configuracion_route(self, client, app):
        """Test 9: GET /configuracion - Configuración carga correctamente."""
        with app.app_context():
            response = client.get('/configuracion')
            assert response.status_code == 200
            # ✅ Verificar texto con acento o sin él
            assert b'Configuraci' in response.data or b'Configuracion' in response.data

    def test_route_404(self, client, app):
        """Test 10: GET /ruta_no_existente - Debe retornar 404."""
        with app.app_context():
            response = client.get('/ruta_no_existente')
            assert response.status_code == 404
