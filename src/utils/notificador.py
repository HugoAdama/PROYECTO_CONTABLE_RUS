# src/utils/notificador.py
"""
📧 NOTIFICADOR POR EMAIL
Envía alertas automáticas por correo electrónico
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class NotificadorEmail:
    """
    Envía notificaciones por email usando SMTP.
    """
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_origen = os.getenv('EMAIL_ORIGEN')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_destino = os.getenv('EMAIL_DESTINO')
    
    def enviar_alerta_limite(self, ventas: float, limite: float = 8000):
        """
        Envía alerta cuando las ventas se acercan al límite RUS.
        
        Args:
            ventas (float): Ventas actuales del mes
            limite (float): Límite RUS (8000 por defecto)
        """
        porcentaje = (ventas / limite) * 100
        mensaje = self._generar_mensaje_limite(ventas, limite, porcentaje)
        
        return self._enviar_email(
            asunto="⚠️ Alerta RUS - Control Financiero",
            mensaje=mensaje
        )
    
    def _generar_mensaje_limite(self, ventas, limite, porcentaje):
        """Genera el mensaje de alerta de límite."""
        
        if porcentaje > 100:
            nivel = "🚨 URGENTE"
            color = "rojo"
            recomendacion = "¡Has superado el límite RUS! Consulta a tu contador inmediatamente."
        elif porcentaje > 90:
            nivel = "⚠️ ADVERTENCIA"
            color = "naranja"
            recomendacion = f"Te faltan S/ {limite - ventas:,.2f} para llegar al límite. Controla tus ventas."
        elif porcentaje > 70:
            nivel = "ℹ️ INFORMACIÓN"
            color = "amarillo"
            recomendacion = f"Estás al {porcentaje:.0f}% del límite RUS. Sigue así."
        else:
            return None
        
        mensaje = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .alert-{color} {{ padding: 15px; border-radius: 8px; margin: 10px 0; }}
                .metric {{ display: inline-block; padding: 10px 20px; background: #f0f0f0; border-radius: 8px; margin: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Control Financiero RUS</h1>
                <p>{nivel}</p>
            </div>
            <div class="content">
                <h2>Estado de tus ventas</h2>
                <div class="alert-{color}">
                    <p><strong>Ventas actuales:</strong> S/ {ventas:,.2f}</p>
                    <p><strong>Límite RUS:</strong> S/ {limite:,.2f}</p>
                    <p><strong>Porcentaje usado:</strong> {porcentaje:.1f}%</p>
                </div>
                <h3>💡 Recomendación</h3>
                <p>{recomendacion}</p>
                <hr>
                <p style="color: #666; font-size: 0.8rem;">
                    Este es un mensaje automático del Sistema de Control Financiero.<br>
                    Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return mensaje
    
    def _enviar_email(self, asunto: str, mensaje: str) -> bool:
        """
        Envía el email usando SMTP.
        
        Returns:
            bool: True si se envió correctamente
        """
        if not self.email_origen or not self.email_password:
            print("⚠️ Credenciales de email no configuradas")
            return False
        
        if not self.email_destino:
            print("⚠️ Email de destino no configurado")
            return False
        
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = self.email_origen
            msg['To'] = self.email_destino
            msg['Subject'] = asunto
            
            # Agregar contenido HTML
            msg.attach(MIMEText(mensaje, 'html'))
            
            # Conectar y enviar
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_origen, self.email_password)
                server.send_message(msg)
            
            print(f"✅ Email enviado a {self.email_destino}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar email: {e}")
            return False
    
    def enviar_resumen_mensual(self, resumen: dict, mes: int, año: int):
        """
        Envía un resumen mensual por email.
        
        Args:
            resumen (dict): Resumen financiero del mes
            mes (int): Mes
            año (int): Año
        """
        nombre_mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"][mes-1]
        
        mensaje = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .metric-card {{ display: inline-block; padding: 15px 25px; background: #f8f9fa; border-radius: 10px; margin: 5px; min-width: 120px; text-align: center; }}
                .metric-value {{ font-size: 1.5rem; font-weight: bold; color: #2d3436; }}
                .metric-label {{ font-size: 0.8rem; color: #636e72; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Resumen Mensual</h1>
                <p>{nombre_mes} {año}</p>
            </div>
            <div class="content">
                <h2>📈 Resumen Financiero</h2>
                <div style="text-align: center;">
                    <div class="metric-card">
                        <div class="metric-value">S/ {resumen['total_ventas']:,.2f}</div>
                        <div class="metric-label">💰 Ventas</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">S/ {resumen['total_compras']:,.2f}</div>
                        <div class="metric-label">📦 Compras</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" style="color: {'#00b894' if resumen['utilidad'] > 0 else '#ff6b6b'}">
                            S/ {resumen['utilidad']:,.2f}
                        </div>
                        <div class="metric-label">💵 Utilidad</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">S/ {resumen['total_percepciones']:,.2f}</div>
                        <div class="metric-label">⭐ Percepciones</div>
                    </div>
                </div>
                <hr>
                <p style="color: #666; font-size: 0.8rem;">
                    Este es un resumen automático del Sistema de Control Financiero.<br>
                    Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._enviar_email(
            asunto=f"📊 Resumen {nombre_mes} {año} - Control Financiero",
            mensaje=mensaje
        )