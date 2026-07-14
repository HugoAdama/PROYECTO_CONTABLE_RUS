/**
 * CORE: SISTEMA DE EVENTOS
 * Sistema de Control Financiero RUS v3.9.1
 */

class EventBus {
    constructor() {
        this.events = {};
    }
    
    /**
     * Suscribirse a un evento
     */
    on(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    }
    
    /**
     * Emitir un evento
     */
    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(callback => callback(data));
        }
    }
    
    /**
     * Eliminar suscripción
     */
    off(event, callback) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(cb => cb !== callback);
        }
    }
}

// ============================================
// INSTANCIA GLOBAL
// ============================================
const eventBus = new EventBus();

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = eventBus;
}