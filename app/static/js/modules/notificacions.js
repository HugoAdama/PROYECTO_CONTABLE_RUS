/**
 * MODULE: NOTIFICATIONS
 * Sistema de notificaciones toast
 */

const NotificationsModule = (function() {
    'use strict';
    
    let container = null;
    const DEFAULTS = {
        duration: 5000,
        position: 'top-right',
    };
    
    /**
     * Crea el contenedor de notificaciones
     */
    function createContainer() {
        if (container) return container;
        
        container = DOM.create('div', {
            id: 'notification-container',
            className: 'notification-container',
            style: `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 380px;
                width: 100%;
                pointer-events: none;
            `,
        });
        
        document.body.appendChild(container);
        return container;
    }
    
    /**
     * Muestra una notificación
     * @param {string} message - Mensaje a mostrar
     * @param {string} type - Tipo: info, success, warning, error
     * @param {Object} options - Opciones adicionales
     */
    function show(message, type = 'info', options = {}) {
        const duration = options.duration || DEFAULTS.duration;
        const container = createContainer();
        
        // Colores según tipo
        const colors = {
            info: { bg: 'rgba(96, 165, 250, 0.15)', border: 'rgba(96, 165, 250, 0.2)', icon: 'fa-info-circle' },
            success: { bg: 'rgba(74, 222, 128, 0.15)', border: 'rgba(74, 222, 128, 0.2)', icon: 'fa-check-circle' },
            warning: { bg: 'rgba(251, 191, 36, 0.15)', border: 'rgba(251, 191, 36, 0.2)', icon: 'fa-exclamation-triangle' },
            error: { bg: 'rgba(248, 113, 113, 0.15)', border: 'rgba(248, 113, 113, 0.2)', icon: 'fa-times-circle' },
        };
        
        const color = colors[type] || colors.info;
        
        // Crear notificación
        const notification = DOM.create('div', {
            className: `notification notification-${type}`,
            style: `
                background: rgba(10, 10, 30, 0.95);
                backdrop-filter: blur(20px);
                border: 1px solid ${color.border};
                border-radius: 12px;
                padding: 14px 18px;
                display: flex;
                align-items: center;
                gap: 12px;
                color: #fff;
                font-size: 0.9rem;
                font-family: 'Inter', sans-serif;
                pointer-events: auto;
                animation: slideInRight 0.4s ease forwards;
                box-shadow: 0 8px 40px rgba(0,0,0,0.3);
                transform: translateX(120%);
            `,
        });
        
        // Icono
        const icon = DOM.create('i', {
            className: `fas ${color.icon}`,
            style: `color: ${color.border}; font-size: 1.2rem; flex-shrink: 0;`,
        });
        
        // Mensaje
        const text = DOM.create('span', {
            style: 'flex: 1;',
        }, message);
        
        // Botón cerrar
        const closeBtn = DOM.create('i', {
            className: 'fas fa-times',
            style: `
                color: rgba(255,255,255,0.2);
                cursor: pointer;
                font-size: 0.9rem;
                transition: color 0.3s ease;
                flex-shrink: 0;
            `,
        });
        
        DOM.on(closeBtn, 'click', () => {
            removeNotification(notification);
        });
        
        notification.appendChild(icon);
        notification.appendChild(text);
        notification.appendChild(closeBtn);
        container.appendChild(notification);
        
        // Auto-remover
        if (duration > 0) {
            setTimeout(() => {
                removeNotification(notification);
            }, duration);
        }
        
        // Agregar animación de salida
        function removeNotification(el) {
            el.style.animation = 'slideOutRight 0.4s ease forwards';
            setTimeout(() => {
                if (el.parentNode) el.parentNode.removeChild(el);
            }, 400);
        }
    }
    
    /**
     * Muestra una notificación de éxito
     */
    function success(message, options = {}) {
        show(message, 'success', options);
    }
    
    /**
     * Muestra una notificación de error
     */
    function error(message, options = {}) {
        show(message, 'error', options);
    }
    
    /**
     * Muestra una notificación de advertencia
     */
    function warning(message, options = {}) {
        show(message, 'warning', options);
    }
    
    /**
     * Muestra una notificación informativa
     */
    function info(message, options = {}) {
        show(message, 'info', options);
    }
    
    // Inyectar animaciones
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(120%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(120%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    
    // API pública
    const api = {
        show: show,
        success: success,
        error: error,
        warning: warning,
        info: info,
    };
    
    // Exponer globalmente
    if (typeof window !== 'undefined') {
        window.Notifications = api;
    }
    
    return api;
})();

// Exponer funciones globales para compatibilidad
window.mostrarNotificacion = NotificationsModule.show;
window.mostrarExito = NotificationsModule.success;
window.mostrarError = NotificationsModule.error;