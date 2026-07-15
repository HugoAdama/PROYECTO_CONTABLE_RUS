/**
 * Sistema de Notificaciones - Alto contraste en ambos modos
 */

(function() {
    "use strict";

    // ============================================
    // MOSTRAR NOTIFICACIÓN
    // ============================================

    window.showNotification = function(message, type) {
        // Crear contenedor si no existe
        let container = document.getElementById("notification-container");
        if (!container) {
            container = document.createElement("div");
            container.id = "notification-container";
            container.style.cssText = `
                position: fixed;
                top: 24px;
                right: 24px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 12px;
                max-width: 420px;
                pointer-events: none;
            `;
            document.body.appendChild(container);
        }

        // Detectar tema actual
        const isDark = document.documentElement.getAttribute("data-theme") === "dark";

        // Crear notificación
        const notification = document.createElement("div");
        
        // Estilos - ALTO CONTRASTE
        notification.style.cssText = `
            background: ${isDark ? '#1a1a2e' : '#ffffff'};
            backdrop-filter: blur(20px);
            padding: 20px 28px;
            border-radius: 16px;
            border: 1px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.06)'};
            color: ${isDark ? '#f7fafc' : '#1a1a2e'};
            font-size: 1.15rem;
            font-weight: 600;
            box-shadow: 0 8px 40px rgba(0,0,0,${isDark ? '0.5' : '0.12'});
            opacity: 0;
            transform: translateX(20px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 16px;
            min-height: 64px;
            pointer-events: auto;
            line-height: 1.5;
        `;

        // Borde lateral según tipo
        const borderColors = {
            info: isDark ? '#60a5fa' : '#3b82f6',
            success: isDark ? '#4ade80' : '#22c55e',
            warning: isDark ? '#fbbf24' : '#eab308',
            error: isDark ? '#f87171' : '#ef4444'
        };
        const color = borderColors[type] || borderColors.info;
        notification.style.borderLeft = `4px solid ${color}`;

        // Icono según tipo
        const icons = {
            info: 'ℹ️',
            success: '✅',
            warning: '⚠️',
            error: '❌'
        };
        const icon = icons[type] || 'ℹ️';

        notification.innerHTML = `<span style="font-size:1.4rem;">${icon}</span> ${message}`;

        // Agregar al contenedor
        container.appendChild(notification);

        // Animar entrada
        requestAnimationFrame(() => {
            notification.style.opacity = "1";
            notification.style.transform = "translateX(0)";
        });

        // Auto-cerrar después de 3.5 segundos
        setTimeout(() => {
            notification.style.opacity = "0";
            notification.style.transform = "translateX(20px)";
            setTimeout(() => {
                notification.remove();
                if (container.children.length === 0) {
                    container.remove();
                }
            }, 400);
        }, 3500);
    };

    // ============================================
    // FUNCIONES DE AYUDA
    // ============================================

    window.Notifications = {
        show: window.showNotification,
        info: function(message) {
            window.showNotification(message, 'info');
        },
        success: function(message) {
            window.showNotification(message, 'success');
        },
        warning: function(message) {
            window.showNotification(message, 'warning');
        },
        error: function(message) {
            window.showNotification(message, 'error');
        }
    };

})();
