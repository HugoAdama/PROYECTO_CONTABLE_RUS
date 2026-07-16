"""
Sistema de alertas para el RUS
"""
from datetime import datetime
from typing import Dict, Any, Optional
from contable.utils.notificador import NotificadorEmail  # ✅ Importación correcta

class SistemaAlertas:
    """Sistema de alertas para el RUS"""
    
    def __init__(self, email_notificaciones: Optional[str] = None):
        self.email_notificaciones = email_notificaciones
        self.notificador_email = NotificadorEmail() if email_notificaciones else None
    
    def verificar_limite_rus(self, ventas: float, limite: float = 8000) -> Dict[str, Any]:
        """
        Verifica si las ventas superan el límite RUS
        
        Args:
            ventas: Ventas del mes
            limite: Límite máximo permitido
        
        Returns:
            Dict con estado, mensaje y color
        """
        if ventas > limite:
            return {
                'estado': 'peligro',
                'mensaje': f'🚨 Límite RUS superado: S/ {ventas:,.2f} > S/ {limite:,.2f}',
                'color': 'danger',
                'icono': '🚨'
            }
        elif ventas > limite * 0.8:
            return {
                'estado': 'alerta',
                'mensaje': f'⚠️ Cerca del límite RUS: S/ {ventas:,.2f} / S/ {limite:,.2f}',
                'color': 'warning',
                'icono': '⚠️'
            }
        else:
            return {
                'estado': 'ok',
                'mensaje': f'✅ Dentro del límite RUS: S/ {ventas:,.2f} / S/ {limite:,.2f}',
                'color': 'success',
                'icono': '✅'
            }
    
    def enviar_alerta_si_es_necesario(self, ventas: float, limite: float = 8000) -> bool:
        """
        Envía una alerta por email si las ventas superan el límite o están cerca
        
        Args:
            ventas: Ventas del mes
            limite: Límite máximo permitido
        
        Returns:
            bool: True si se envió la alerta, False en caso contrario
        """
        if not self.notificador_email or not self.email_notificaciones:
            return False
        
        resultado = self.verificar_limite_rus(ventas, limite)
        estado = resultado.get('estado', 'ok')
        
        if estado != 'ok':
            return self.notificador_email.enviar_alerta_rus(
                self.email_notificaciones,
                ventas,
                estado,
                limite
            )
        
        return False