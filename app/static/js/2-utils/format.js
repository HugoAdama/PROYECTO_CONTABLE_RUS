/**
 * UTILS: FORMATEADORES
 * Sistema de Control Financiero RUS v3.9.1
 */

class FormatUtils {
    /**
     * Formatear moneda (Soles)
     */
    static currency(amount) {
        return `S/ ${Number(amount).toFixed(2)}`;
    }
    
    /**
     * Formatear número con separadores de miles
     */
    static number(value) {
        return Number(value).toLocaleString('es-PE');
    }
    
    /**
     * Formatear porcentaje
     */
    static percent(value) {
        return `${Number(value).toFixed(1)}%`;
    }
    
    /**
     * Formatear fecha
     */
    static date(date, format = 'dd/mm/yyyy') {
        if (!date) return '-';
        const d = new Date(date);
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        
        return format
            .replace('dd', day)
            .replace('mm', month)
            .replace('yyyy', year);
    }
    
    /**
     * Formatear fecha con hora
     */
    static datetime(date) {
        if (!date) return '-';
        const d = new Date(date);
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        
        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }
    
    /**
     * Truncar texto
     */
    static truncate(text, length = 30) {
        if (!text) return '';
        return text.length > length ? text.substring(0, length) + '...' : text;
    }
    
    /**
     * Capitalizar texto
     */
    static capitalize(text) {
        if (!text) return '';
        return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
    }
    
    /**
     * Formatear tamaño de archivo
     */
    static fileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
    }
}

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FormatUtils;
}