/**
 * UTILS: VALIDADORES
 * Sistema de Control Financiero RUS v3.9.1
 */

class Validators {
    /**
     * Validar email
     */
    static isEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
    
    /**
     * Validar URL
     */
    static isUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }
    
    /**
     * Validar número
     */
    static isNumber(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    }
    
    /**
     * Validar que no esté vacío
     */
    static isNotEmpty(value) {
        return value && value.trim().length > 0;
    }
    
    /**
     * Validar longitud mínima
     */
    static minLength(value, length) {
        return value && value.length >= length;
    }
    
    /**
     * Validar archivo PDF
     */
    static isPDF(file) {
        return file && (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf'));
    }
}

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Validators;
}