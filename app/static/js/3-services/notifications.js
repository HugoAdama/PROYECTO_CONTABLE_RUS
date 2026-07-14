/**
 * SERVICES: SISTEMA DE NOTIFICACIONES
 * Sistema de Control Financiero RUS v3.9.1
 */

import { APP_CONFIG } from '../1-core/config.js';

class NotificationService {
    constructor() {
        this.container = null;
        this.defaultDuration = APP_CONFIG.NOTIFICACIONES.DURACION;
        this.init();
    }
    
    /**
     * Inicializar
     */
    init() {
        this.createContainer();
        this.setupGlobalHandler();
    }
    
    /**
     * Crear contenedor
     */
    createContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = `
                position: fixed;
                top: 24px;
                right: 24px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 12px;
                max-width: 420px;
                width: 100%;
                pointer-events: none;
            `;
            document.body.appendChild(container);
        }
        this.container = container;
    }
    
    /**
     * Configurar handler global
     */
    setupGlobalHandler() {
        window.mostrarNotificacion = (mensaje, tipo = 'info', duracion = this.defaultDuration) => {
            this.show(mensaje, tipo, duracion);
        };
    }
    
    /**
     * Mostrar notificación
     */
    show(mensaje, tipo = 'info', duracion = 4000) {
        const colores = {
            success: '#4ade80',
            error: '#f87171',
            warning: '#fbbf24',
            info: '#60a5fa'
        };
        
        const iconos = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        const toast = document.createElement('div');
        toast.style.cssText = `
            background: var(--bg-card, rgba(15, 23, 42, 0.95));
            backdrop-filter: blur(24px);
            border: 1px solid ${colores[tipo] || colores.info};
            border-radius: 16px;
            padding: 18px 22px;
            color: var(--text-primary, white);
            font-size: 1.1rem;
            font-weight: 500;
            box-shadow: var(--shadow-xl, 0 12px 50px rgba(0,0,0,0.4));
            animation: slideIn 0.3s ease;
            pointer-events: auto;
            display: flex;
            align-items: center;
            gap: 14px;
        `;
        
        toast.innerHTML = `
            <span style="font-size:24px; flex-shrink:0;">${iconos[tipo] || 'ℹ️'}</span>
            <span style="flex:1;">${mensaje}</span>
            <button onclick="this.parentElement.remove()" style="
                background:none;
                border:none;
                color:var(--text-tertiary, rgba(255,255,255,0.4));
                font-size:20px;
                cursor:pointer;
                padding:0 6px;
            ">✕</button>
        `;
        
        this.container.appendChild(toast);
        
        // Auto-eliminar
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100px)';
                toast.style.transition = 'all 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, duracion);
    }
    
    /**
     * Notificación de éxito
     */
    success(mensaje, duracion) {
        this.show(mensaje, 'success', duracion);
    }
    
    /**
     * Notificación de error
     */
    error(mensaje, duracion) {
        this.show(mensaje, 'error', duracion);
    }
    
    /**
     * Notificación de advertencia
     */
    warning(mensaje, duracion) {
        this.show(mensaje, 'warning', duracion);
    }
    
    /**
     * Notificación de información
     */
    info(mensaje, duracion) {
        this.show(mensaje, 'info', duracion);
    }
}

// ============================================
// INSTANCIA GLOBAL
// ============================================
const notifications = new NotificationService();

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = notifications;
}