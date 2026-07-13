/**
 * CONFIGURACIÓN GLOBAL
 * Variables de configuración para toda la aplicación
 */

const APP_CONFIG = {
    // API endpoints
    API: {
        REPORTES_DATOS: '/api/reportes/datos',
        EXPORTAR_EXCEL: '/exportar/excel',
    },
    
    // Paginación
    PAGINATION: {
        DEFAULT_PER_PAGE: 10,
        PER_PAGE_OPTIONS: [5, 10, 25, 50],
    },
    
    // Notificaciones
    NOTIFICATIONS: {
        DURATION: 5000, // milisegundos
        POSITION: 'top-right',
    },
    
    // Formato
    FORMAT: {
        LOCALE: 'es-PE',
        CURRENCY: 'PEN',
        DATE_FORMAT: 'dd/MM/yyyy',
    },
    
    // Upload
    UPLOAD: {
        MAX_FILE_SIZE: 52428800, // 50MB
        ALLOWED_TYPES: ['application/pdf'],
    },
};

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.APP_CONFIG = APP_CONFIG;
}