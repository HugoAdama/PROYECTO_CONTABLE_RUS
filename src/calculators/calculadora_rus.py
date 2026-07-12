# src/calculators/calculadora_rus.py
class CalculadoraRUS:
    LIMITE_MENSUAL = 8000
    LIMITE_ALERTA = 7800
    MONTO_BAJO = 5000

    def __init__(self, ventas_mes, mes=None, anio=None):
        self.ventas = ventas_mes
        self.mes = mes
        self.anio = anio

    def calcular_impuesto(self):
        if self.ventas < self.MONTO_BAJO:
            return 20
        else:
            return 50

    def obtener_estado(self):
        if self.ventas > self.LIMITE_MENSUAL:
            return {'estado': 'excedido', 'mensaje': '🔴 HAS EXCEDIDO EL LÍMITE!', 'color': 'danger', 'icono': '🚨'}
        elif self.ventas >= self.LIMITE_ALERTA:
            return {'estado': 'alerta', 'mensaje': f'⚠️ ¡Cuidado! Estás a S/ {self.LIMITE_MENSUAL - self.ventas:,.2f} del límite', 'color': 'warning', 'icono': '⚠️'}
        else:
            porcentaje = (self.ventas / self.LIMITE_MENSUAL) * 100
            return {'estado': 'ok', 'mensaje': f'✅ Bien, estás al {porcentaje:.1f}% del límite', 'color': 'success', 'icono': '✅'}