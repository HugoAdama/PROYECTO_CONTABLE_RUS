# src/calculators/calculadora_rus.py
class CalculadoraRUS:
    """Calculadora para el Régimen Único Simplificado"""
    
    LIMITE_MENSUAL = 8000
    IMPUESTO_NORMAL = 20
    IMPUESTO_ALERTA = 50
    
    @staticmethod
    def calcular_estado(ventas_mensuales):
        """
        Calcula el estado del contribuyente según sus ventas mensuales
        Retorna: (estado, impuesto)
        """
        if ventas_mensuales <= 5000:
            return 'normal', CalculadoraRUS.IMPUESTO_NORMAL
        elif ventas_mensuales <= CalculadoraRUS.LIMITE_MENSUAL:
            return 'alerta', CalculadoraRUS.IMPUESTO_ALERTA
        else:
            return 'urgente', 0
    
    @staticmethod
    def calcular_impuesto_final(ventas, percepciones):
        """Calcula el impuesto final después de percepciones"""
        impuesto_base = ventas * 0.05
        return max(0, impuesto_base - percepciones)
    
    @staticmethod
    def esta_dentro_limite(ventas_mensuales):
        """Verifica si las ventas están dentro del límite mensual"""
        return ventas_mensuales <= CalculadoraRUS.LIMITE_MENSUAL
    
    @staticmethod
    def get_alerta(ventas_mensuales):
        """Obtiene el nivel de alerta según las ventas"""
        if ventas_mensuales <= 5000:
            return 'success'
        elif ventas_mensuales <= CalculadoraRUS.LIMITE_MENSUAL:
            return 'warning'
        else:
            return 'danger'