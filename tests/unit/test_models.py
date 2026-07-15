"""
Pruebas unitarias con DATOS REALES de Doña María.
"""
import pytest

class TestFacturasReales:
    def test_factura_30022(self, factura_30022):
        assert factura_30022.monto == 750.13
        # ✅ Cambiar a mayúsculas (como viene del extractor)
        assert factura_30022.proveedor == 'NATURA COSMETICOS S.A.'
        assert factura_30022.numero == 'F033-00330022'

    def test_factura_30623(self, factura_30623):
        assert factura_30623.monto == 191.70
        assert factura_30623.proveedor == 'NATURA COSMETICOS S.A.'
        assert factura_30623.numero == 'F033-00330623'

    def test_factura_31167(self, factura_31167):
        assert factura_31167.monto == 450.37
        assert factura_31167.proveedor == 'NATURA COSMETICOS S.A.'
        assert factura_31167.numero == 'F033-00331167'

    def test_total_compras_mayo(self, factura_30022, factura_30623, factura_31167):
        total = factura_30022.monto + factura_30623.monto + factura_31167.monto
        assert total == pytest.approx(1392.20, 0.01)

class TestBoletasReales:
    def test_boleta_302(self, boleta_302):
        assert boleta_302.monto == 200.00
        # ✅ Usar el cliente real del PDF
        assert boleta_302.cliente == 'KAROLAY CHAVEZ'
        assert boleta_302.numero == 'EB01-302'

    def test_boleta_303(self, boleta_303):
        assert boleta_303.monto == 220.00
        assert boleta_303.cliente == 'INACIA CHU'
        assert boleta_303.numero == 'EB01-303'

    def test_boleta_304(self, boleta_304):
        assert boleta_304.monto == 140.00
        assert boleta_304.cliente == 'BEICY VAR'
        assert boleta_304.numero == 'EB01-304'

    def test_total_ventas_mayo(self, boleta_302, boleta_303, boleta_304):
        total = boleta_302.monto + boleta_303.monto + boleta_304.monto
        assert total == 560.00

class TestPercepcionReal:
    def test_percepcion_monto(self, percepcion_real):
        assert percepcion_real.monto == 441.54
        assert percepcion_real.numero == 'P003-00602821'

class TestEstadoRUS:
    def test_calculo_impuesto_base(self):
        ventas = 560.00
        esperado = 560.00 * 0.05
        from src.calculators.calculadora_rus import CalculadoraRUS
        resultado = CalculadoraRUS.calcular_impuesto_final(ventas, 0)
        assert resultado == pytest.approx(esperado, 0.01)

    def test_calculo_impuesto_con_percepcion(self):
        ventas = 560.00
        percepciones = 8.83
        impuesto_base = 560.00 * 0.05
        esperado = impuesto_base - percepciones
        from src.calculators.calculadora_rus import CalculadoraRUS
        resultado = CalculadoraRUS.calcular_impuesto_final(ventas, percepciones)
        assert resultado == pytest.approx(esperado, 0.01)

    def test_limite_rus_seguro(self):
        ventas = 560.00
        limite = 8000.00
        diferencia = limite - ventas
        assert diferencia == 7440.00
        assert diferencia > 0
