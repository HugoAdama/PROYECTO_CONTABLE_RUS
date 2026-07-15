/**
 * CORE: CONFIGURACIÓN GLOBAL
 * Sistema de Control Financiero RUS v3.9.1
 */

const APP_CONFIG = {
    // ==========================================
    // VERSIÓN
    // ==========================================
    VERSION: '3.9.1',
    
    // ==========================================
    // URLS DE LA API
    // ==========================================
    API: {
        ORGANIZAR_CARPETAS: '/api/organizar-carpetas',
        REPORTES_DATOS: '/api/reportes/datos',
        GUARDAR_CONFIG: '/api/configuracion/guardar',
    },
    
    // ==========================================
    // CLAVES DE LOCALSTORAGE
    // ==========================================
    STORAGE: {
        TEMA: 'rus_tema',
        COLOR_PRIMARIO: 'rus_color_primario',
        NOMBRE_NEGOCIO: 'rus_nombre_negocio',
        EMAIL_NOTIFICACIONES: 'rus_email_notificaciones',
        NOTIFICACIONES_ACTIVAS: 'rus_notificaciones_activas',
    },
    
    // ==========================================
    // CONFIGURACIÓN DE NOTIFICACIONES
    // ==========================================
    NOTIFICACIONES: {
        DURACION: 4000,
        POSICION: 'top-right',
    },
    
    // ==========================================
    // CONFIGURACIÓN DE PAGINACIÓN
    // ==========================================
    PAGINACION: {
        POR_PAGINA: 10,
        MAX_VISIBLE: 5,
    },
    
    // ==========================================
    // SELECTORES CSS
    // ==========================================
    SELECTORES: {
        SIDEBAR: '#sidebar',
        SIDEBAR_TOGGLE: '#sidebarToggle',
        SIDEBAR_OVERLAY: '#sidebarOverlay',
        MAIN_CONTENT: '#mainContent',
        TOAST_CONTAINER: '#toast-container',
    },
};

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APP_CONFIG;
}