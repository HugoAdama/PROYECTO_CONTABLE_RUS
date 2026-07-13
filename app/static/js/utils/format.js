/**
 * UTILIDADES DE FORMATO
 * Formateadores de moneda, fecha, números
 */

const FORMAT = {
    /**
     * Formatea un número como moneda (Soles)
     * @param {number} value - Valor a formatear
     * @param {string} locale - Locale (default: es-PE)
     * @param {string} currency - Moneda (default: PEN)
     * @returns {string}
     */
    currency: (value, locale = 'es-PE', currency = 'PEN') => {
        if (value === null || value === undefined || isNaN(value)) {
            return 'S/ 0.00';
        }
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(value);
    },
    
    /**
     * Formatea un número con separadores de miles
     * @param {number} value - Valor a formatear
     * @param {string} locale - Locale (default: es-PE)
     * @returns {string}
     */
    number: (value, locale = 'es-PE') => {
        if (value === null || value === undefined || isNaN(value)) {
            return '0';
        }
        return new Intl.NumberFormat(locale).format(value);
    },
    
    /**
     * Formatea una fecha
     * @param {string|Date} date - Fecha a formatear
     * @param {string} format - Formato (default: 'dd/MM/yyyy')
     * @returns {string}
     */
    date: (date, format = 'dd/MM/yyyy') => {
        if (!date) return '-';
        
        const d = typeof date === 'string' ? new Date(date) : date;
        if (!(d instanceof Date) || isNaN(d)) return '-';
        
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        
        return format
            .replace('dd', day)
            .replace('MM', month)
            .replace('yyyy', year);
    },
    
    /**
     * Formatea un porcentaje
     * @param {number} value - Valor
     * @param {number} decimals - Decimales (default: 1)
     * @returns {string}
     */
    percent: (value, decimals = 1) => {
        if (value === null || value === undefined || isNaN(value)) {
            return '0%';
        }
        return value.toFixed(decimals) + '%';
    },
    
    /**
     * Trunca un texto a una longitud máxima
     * @param {string} text - Texto a truncar
     * @param {number} maxLength - Longitud máxima
     * @param {string} suffix - Sufijo (default: '...')
     * @returns {string}
     */
    truncate: (text, maxLength = 50, suffix = '...') => {
        if (!text) return '-';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + suffix;
    },
};

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.FORMAT = FORMAT;
}