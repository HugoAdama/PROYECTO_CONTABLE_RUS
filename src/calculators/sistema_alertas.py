# src/calculators/sistema_alertas.py - Agregar notificación por email

from .calculadora_rus import CalculadoraRUS
from src.utils.notificador import NotificadorEmail

class SistemaAlertas:
    """Sistema de alertas con notificaciones por email."""
    
    def __init__(self, mes, año):
        self.mes = mes
        self.año = año
        self.calculadora = CalculadoraRUS(mes, año)
        self.notificador = NotificadorEmail()
    
    def verificar_todas(self):
        """Verifica todas las alertas y envía notificaciones si es necesario."""
        alertas = []
        
        # 1. Alerta de límite RUS
        nivel, mensaje = self.calculadora.verificar_limite()
        if mensaje:
            alertas.append({'nivel': nivel, 'mensaje': mensaje})
            
            # Enviar email si es crítica o advertencia
            if nivel in ['CRITICAL', 'WARNING']:
                self._enviar_alerta_limite()
        
        # 2. Alerta de impuestos
        resultado = self.calculadora.calcular_impuesto_real()
        if resultado['error']:
            alertas.append({'nivel': 'CRITICAL', 'mensaje': resultado['mensaje']})
        elif resultado['ahorro'] > 0:
            alertas.append({
                'nivel': 'SUCCESS',
                'mensaje': f'✅ Ahorraste S/ {resultado["ahorro"]:.2f} en impuestos'
            })
        
        return alertas
    
    def _enviar_alerta_limite(self):
        """Envía alerta de límite por email."""
        ventas = self.calculadora.ventas_totales
        self.notificador.enviar_alerta_limite(ventas)
    
    def enviar_resumen_mensual(self, resumen):
        """Envía resumen mensual por email."""
        return self.notificador.enviar_resumen_mensual(resumen, self.mes, self.año)