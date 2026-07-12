# src/calculators/calculadora_rus.py
"""
Calculadora de impuestos para el Régimen Único Simplificado (RUS)
"""

class CalculadoraRUS:
    """Calculadora de impuestos para el Régimen Único Simplificado"""
    
    def __init__(self, mes, año):
        self.mes = mes
        self.año = año
        self.ventas_totales = 0.0
        self.total_percepciones = 0.0
    
    def calcular_impuesto_base(self):
        """Calcula el impuesto base según el RUS"""
        if self.ventas_totales <= 3000:
            return 20.00
        elif self.ventas_totales <= 8000:
            return 50.00
        else:
            return None  # Excede el límite
    
    def calcular_impuesto_real(self):
        """Calcula el impuesto REAL restando percepciones"""
        impuesto_base = self.calcular_impuesto_base()
        
        if impuesto_base is None:
            return {
                'error': True,
                'mensaje': '❌ Excediste el límite RUS (S/ 8,000)'
            }
        
        ahorro = min(impuesto_base, self.total_percepciones)
        impuesto_final = impuesto_base - ahorro
        
        return {
            'error': False,
            'impuesto_base': impuesto_base,
            'total_percepciones': self.total_percepciones,
            'ahorro': ahorro,
            'impuesto_final': impuesto_final,
            'percepciones_restantes': self.total_percepciones - ahorro
        }
    
    def verificar_limite(self):
        """Verifica si está cerca del límite RUS"""
        if self.ventas_totales > 8000:
            return 'CRITICAL', f'🚨 Ventas: S/ {self.ventas_totales:.2f} - EXCEDES EL LÍMITE'
        elif self.ventas_totales >= 7500:
            diferencia = 8000 - self.ventas_totales
            return 'WARNING', f'⚠️ Ventas: S/ {self.ventas_totales:.2f} - Te faltan S/ {diferencia:.2f}'
        return 'OK', None