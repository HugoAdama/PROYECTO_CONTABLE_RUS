/**
 * app.js - Archivo principal de JavaScript
 * Contiene utilidades y configuraciones globales
 */

// ============================================================
// UTILIDADES GENERALES
// ============================================================

/**
 * Formatea un número como moneda S/ (soles peruanos)
 * @param {number} valor - El valor a formatear
 * @param {number} decimales - Número de decimales (por defecto 2)
 * @returns {string} Valor formateado como S/ 1,234.56
 */
function formatearMoneda(valor, decimales = 2) {
    if (valor === null || valor === undefined || isNaN(valor)) {
        return 'S/ 0.00';
    }
    return 'S/ ' + Number(valor).toLocaleString('es-PE', {
        minimumFractionDigits: decimales,
        maximumFractionDigits: decimales
    });
}

/**
 * Formatea una fecha de YYYY-MM-DD a DD/MM/YYYY
 * @param {string} fechaStr - Fecha en formato YYYY-MM-DD
 * @returns {string} Fecha en formato DD/MM/YYYY
 */
function formatearFecha(fechaStr) {
    if (!fechaStr) return '-';
    const partes = fechaStr.split('-');
    if (partes.length !== 3) return fechaStr;
    return `${partes[2]}/${partes[1]}/${partes[0]}`;
}

/**
 * Trunca un texto a una longitud máxima
 * @param {string} texto - El texto a truncar
 * @param {number} maxLength - Longitud máxima
 * @returns {string} Texto truncado con '...' si es necesario
 */
function truncarTexto(texto, maxLength = 30) {
    if (!texto) return '';
    if (texto.length <= maxLength) return texto;
    return texto.substring(0, maxLength) + '...';
}

/**
 * Obtiene el nombre del mes a partir de un número (1-12)
 * @param {number} mes - Número del mes (1-12)
 * @returns {string} Nombre del mes
 */
function obtenerNombreMes(mes) {
    const meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];
    return meses[mes - 1] || mes;
}

// ============================================================
// CONFIGURACIÓN DE NOTIFICACIONES GLOBALES
// ============================================================

// Exponer utilidades al objeto global
window.utils = {
    formatearMoneda,
    formatearFecha,
    truncarTexto,
    obtenerNombreMes
};

// ============================================================
// MANEJO DE ERRORES GLOBAL
// ============================================================

// Capturar errores no manejados para mostrar notificaciones
window.addEventListener('unhandledrejection', function(event) {
    console.error('Error no manejado:', event.reason);
    if (window.notificaciones) {
        notificaciones.toast('error', 
            'Ocurrió un error inesperado. Por favor, recarga la página.', 
            'Error del sistema'
        );
    }
});

console.log('✅ Sistema Contable RUS - JavaScript cargado correctamente');
console.log('📌 Versión: 3.2 - Julio 2026');