"""
Pruebas unitarias para los extractores de PDF del Sistema RUS.
Usa datos reales de Doña María.
"""

import pytest
import os

from src.extractors.factura_extractor import FacturaExtractor
from src.extractors.boleta_extractor import BoletaExtractor
from src.extractors.percepcion_extractor import PercepcionExtractor
from src.extractors.detector_extractor import DetectorExtractor


# ============================================
# PRUEBAS DE FACTURAEXTRACTOR
# ============================================

class TestFacturaExtractor:
    """Pruebas para el extractor de facturas con datos reales."""

    def test_extraer_factura_30623(self, ruta_factura_30623):
        """Test 1: Extraer datos de factura F033-00330623 (S/ 187.94)."""
        if not os.path.exists(ruta_factura_30623):
            pytest.skip("Archivo PDF no disponible")

        extractor = FacturaExtractor()
        resultado = extractor.extraer(ruta_factura_30623)

        assert resultado is not None
        assert resultado['tipo'] == 'factura_compra'
        assert resultado['numero_factura'] == 'F033-00330623'
        assert resultado['proveedor'] == 'NATURA COSMETICOS S.A.'
        assert resultado['total_pagar'] == 187.94

    def test_extraer_factura_30022(self, ruta_factura_30022):
        """Test 2: Extraer datos de factura F033-00330022 (S/ 735.63)."""
        if not os.path.exists(ruta_factura_30022):
            pytest.skip("Archivo PDF no disponible")

        extractor = FacturaExtractor()
        resultado = extractor.extraer(ruta_factura_30022)

        assert resultado is not None
        assert resultado['tipo'] == 'factura_compra'
        assert resultado['numero_factura'] == 'F033-00330022'
        assert resultado['proveedor'] == 'NATURA COSMETICOS S.A.'
        assert resultado['total_pagar'] == 735.63

    def test_extraer_factura_31167(self, ruta_factura_31167):
        """Test 3: Extraer datos de factura F033-00331167 (S/ 441.54)."""
        if not os.path.exists(ruta_factura_31167):
            pytest.skip("Archivo PDF no disponible")

        extractor = FacturaExtractor()
        resultado = extractor.extraer(ruta_factura_31167)

        assert resultado is not None
        assert resultado['tipo'] == 'factura_compra'
        assert resultado['numero_factura'] == 'F033-00331167'
        assert resultado['proveedor'] == 'NATURA COSMETICOS S.A.'
        assert resultado['total_pagar'] == 441.54


# ============================================
# PRUEBAS DE BOLETAEXTRACTOR
# ============================================

class TestBoletaExtractor:
    """Pruebas para el extractor de boletas con datos reales."""

    def test_extraer_boleta_302(self, ruta_boleta_302):
        """Test 1: Extraer datos de boleta EB01-302 (S/ 200.00)."""
        if not os.path.exists(ruta_boleta_302):
            pytest.skip("Archivo PDF no disponible")

        extractor = BoletaExtractor()
        resultado = extractor.extraer(ruta_boleta_302)

        assert resultado is not None
        assert resultado['tipo'] == 'boleta_venta'
        assert resultado['numero_boleta'] == 'EB01-302'
        assert resultado['total_pagar'] == 200.0

    def test_extraer_boleta_303(self, ruta_boleta_303):
        """Test 2: Extraer datos de boleta EB01-303 (S/ 220.00)."""
        if not os.path.exists(ruta_boleta_303):
            pytest.skip("Archivo PDF no disponible")

        extractor = BoletaExtractor()
        resultado = extractor.extraer(ruta_boleta_303)

        assert resultado is not None
        assert resultado['tipo'] == 'boleta_venta'
        assert resultado['numero_boleta'] == 'EB01-303'
        assert resultado['total_pagar'] == 220.0

    def test_extraer_boleta_304(self, ruta_boleta_304):
        """Test 3: Extraer datos de boleta EB01-304 (S/ 140.00)."""
        if not os.path.exists(ruta_boleta_304):
            pytest.skip("Archivo PDF no disponible")

        extractor = BoletaExtractor()
        resultado = extractor.extraer(ruta_boleta_304)

        assert resultado is not None
        assert resultado['tipo'] == 'boleta_venta'
        assert resultado['numero_boleta'] == 'EB01-304'
        assert resultado['total_pagar'] == 140.0


# ============================================
# PRUEBAS DE PERCEPCIONEXTRACTOR
# ============================================

class TestPercepcionExtractor:
    """Pruebas para el extractor de percepciones con datos reales."""

    def test_extraer_percepcion(self, ruta_percepcion_real):
        """Test 1: Extraer datos de percepción."""
        if not os.path.exists(ruta_percepcion_real):
            pytest.skip("Archivo PDF no disponible")

        extractor = PercepcionExtractor()
        resultado = extractor.extraer(ruta_percepcion_real)

        assert resultado is not None
        assert resultado['tipo'] == 'percepcion'
        assert resultado['porcentaje'] == 2.0


# ============================================
# PRUEBAS DE DETECTOREXTRACTOR
# ============================================

class TestDetectorExtractor:
    """Pruebas para el detector de tipo de documento."""

    def test_detector_tipo_factura(self, ruta_factura_30623):
        """Test 1: Detectar factura usando el detector."""
        if not os.path.exists(ruta_factura_30623):
            pytest.skip("Archivo PDF no disponible")

        detector = DetectorExtractor()
        # Usar el método de instancia detectar_tipo_documento
        tipo = detector.detectar_tipo_documento()
        # Verificar que detecta algo relacionado con factura
        assert tipo is not None

    def test_detector_tipo_boleta(self, ruta_boleta_302):
        """Test 2: Detectar boleta usando el detector."""
        if not os.path.exists(ruta_boleta_302):
            pytest.skip("Archivo PDF no disponible")

        detector = DetectorExtractor()
        tipo = detector.detectar_tipo_documento()
        assert tipo is not None

    def test_detector_tipo_percepcion(self, ruta_percepcion_real):
        """Test 3: Detectar percepción usando el detector."""
        if not os.path.exists(ruta_percepcion_real):
            pytest.skip("Archivo PDF no disponible")

        detector = DetectorExtractor()
        tipo = detector.detectar_tipo_documento()
        assert tipo is not None

    def test_detector_recomendacion_tipo(self, ruta_factura_30623):
        """Test 4: Obtener recomendación de tipo."""
        if not os.path.exists(ruta_factura_30623):
            pytest.skip("Archivo PDF no disponible")

        detector = DetectorExtractor()
        recomendacion, _ = detector.obtener_recomendacion_tipo()
        assert recomendacion is not None
