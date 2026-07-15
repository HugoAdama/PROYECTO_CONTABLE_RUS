"""
Sistema de notificaciones para la interfaz de usuario y emails
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notificador:
    """Gestor de notificaciones para la UI (toasts, alertas, progreso)"""
    
    @staticmethod
    def crear_toast(tipo: str, mensaje: str, titulo: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea una notificación toast para la UI
        
        Args:
            tipo: 'success', 'error', 'warning', 'info'
            mensaje: Texto principal de la notificación
            titulo: Título opcional de la notificación
        """
        colores = {
            'success': 'bg-success',
            'error': 'bg-danger',
            'warning': 'bg-warning',
            'info': 'bg-info'
        }
        iconos = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        return {
            'tipo': tipo,
            'titulo': titulo or tipo.capitalize(),
            'mensaje': mensaje,
            'color': colores.get(tipo, 'bg-secondary'),
            'icono': iconos.get(tipo, '📢'),
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def crear_alerta(tipo: str, mensaje: str, acciones: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Crea una alerta interactiva para la UI
        
        Args:
            tipo: 'success', 'error', 'warning', 'info'
            mensaje: Texto principal de la alerta
            acciones: Lista de acciones (botones) para la alerta
        """
        colores = {
            'success': '#38ef7d',
            'error': '#eb3349',
            'warning': '#f7971e',
            'info': '#4facfe'
        }
        
        return {
            'tipo': tipo,
            'mensaje': mensaje,
            'color': colores.get(tipo, '#667eea'),
            'acciones': acciones or [],
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def crear_progreso(titulo: str, total: int, actual: int = 0) -> Dict[str, Any]:
        """
        Crea un objeto de progreso para la UI
        
        Args:
            titulo: Descripción del proceso
            total: Número total de elementos
            actual: Elementos procesados actualmente
        """
        porcentaje = (actual / total * 100) if total > 0 else 0
        
        return {
            'titulo': titulo,
            'total': total,
            'actual': actual,
            'porcentaje': min(porcentaje, 100),
            'mensaje': f'Procesando {actual} de {total}...'
        }


# ============================================================
# CLASE NotificadorEmail - Para envío de correos electrónicos
# ============================================================

class NotificadorEmail:
    """
    Clase para enviar notificaciones por correo electrónico
    """
    
    def __init__(self, smtp_server: str = 'smtp.gmail.com', smtp_port: int = 587, 
                 email_remitente: str = None, password: str = None):
        """
        Inicializa el notificador de email
        
        Args:
            smtp_server: Servidor SMTP (ej: smtp.gmail.com)
            smtp_port: Puerto SMTP (587 para TLS)
            email_remitente: Email del remitente
            password: Contraseña del remitente
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_remitente = email_remitente
        self.password = password
    
    def enviar_alerta(self, destinatario: str, asunto: str, mensaje: str) -> bool:
        """
        Envía una alerta por correo electrónico
        
        Args:
            destinatario: Email del destinatario
            asunto: Asunto del correo
            mensaje: Cuerpo del mensaje
        
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        if not all([self.email_remitente, self.password, destinatario]):
            print("⚠️ No se puede enviar email: faltan credenciales")
            return False
        
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = self.email_remitente
            msg['To'] = destinatario
            msg['Subject'] = asunto
            
            # Agregar cuerpo
            msg.attach(MIMEText(mensaje, 'plain', 'utf-8'))
            
            # Conectar y enviar
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_remitente, self.password)
                server.send_message(msg)
            
            print(f"✅ Email enviado a {destinatario}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar email: {e}")
            return False
    
    def enviar_alerta_rus(self, destinatario: str, ventas: float, estado: str, 
                          limite: float = 8000) -> bool:
        """
        Envía una alerta específica del RUS
        
        Args:
            destinatario: Email del destinatario
            ventas: Ventas del mes
            estado: Estado del RUS ('ok', 'alerta', 'peligro')
            limite: Límite máximo de ventas
        """
        estados_mensaje = {
            'ok': '✅ Todo en orden. Tus ventas están dentro del límite RUS.',
            'alerta': f'⚠️ Estás cerca del límite RUS (S/ {limite:,.2f}). Ventas actuales: S/ {ventas:,.2f}',
            'peligro': f'🚨 HAS SUPERADO EL LÍMITE RUS (S/ {limite:,.2f}). Ventas actuales: S/ {ventas:,.2f}.'
        }
        
        mensaje = f"""
        📊 REPORTE RUS - {datetime.now().strftime('%d/%m/%Y')}
        
        {estados_mensaje.get(estado, 'Estado desconocido')}
        
        📈 Ventas del mes: S/ {ventas:,.2f}
        📉 Límite permitido: S/ {limite:,.2f}
        
        ---
        Este es un mensaje automático del Sistema de Control Financiero RUS.
        """
        
        asunto = f"🚨 Alerta RUS - {estado.upper()}" if estado != 'ok' else "✅ Reporte RUS - Todo en orden"
        
        return self.enviar_alerta(destinatario, asunto, mensaje)
    
    def enviar_resumen_mensual(self, destinatario: str, datos: Dict[str, Any]) -> bool:
        """
        Envía un resumen mensual del estado financiero
        
        Args:
            destinatario: Email del destinatario
            datos: Diccionario con los datos del resumen
        """
        ventas = datos.get('ventas', 0)
        compras = datos.get('compras', 0)
        utilidad = datos.get('utilidad', 0)
        impuesto = datos.get('impuesto', 0)
        mes = datos.get('mes', 'Mes')
        anio = datos.get('anio', 'Año')
        
        mensaje = f"""
        📊 RESUMEN FINANCIERO - {mes} {anio}
        
        📈 Ventas: S/ {ventas:,.2f}
        📉 Compras: S/ {compras:,.2f}
        💰 Utilidad: S/ {utilidad:,.2f}
        🏛️ Impuesto RUS: S/ {impuesto:,.2f}
        
        ---
        Este es un resumen automático del Sistema de Control Financiero RUS.
        """
        
        asunto = f"📊 Resumen Financiero - {mes} {anio}"
        
        return self.enviar_alerta(destinatario, asunto, mensaje)