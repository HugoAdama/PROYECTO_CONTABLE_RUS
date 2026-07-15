/**
 * UTILS: MANIPULACIÓN DOM
 * Sistema de Control Financiero RUS v3.9.1
 */

class DOMUtils {
    /**
     * Seleccionar elemento
     */
    static $(selector, context = document) {
        return context.querySelector(selector);
    }
    
    /**
     * Seleccionar todos los elementos
     */
    static $$(selector, context = document) {
        return [...context.querySelectorAll(selector)];
    }
    
    /**
     * Crear elemento
     */
    static create(tag, className = '', attributes = {}) {
        const el = document.createElement(tag);
        if (className) el.className = className;
        Object.keys(attributes).forEach(key => {
            el.setAttribute(key, attributes[key]);
        });
        return el;
    }
    
    /**
     * Añadir clase
     */
    static addClass(el, className) {
        if (el) el.classList.add(className);
    }
    
    /**
     * Eliminar clase
     */
    static removeClass(el, className) {
        if (el) el.classList.remove(className);
    }
    
    /**
     * Alternar clase
     */
    static toggleClass(el, className) {
        if (el) el.classList.toggle(className);
    }
    
    /**
     * Verificar si tiene clase
     */
    static hasClass(el, className) {
        return el ? el.classList.contains(className) : false;
    }
    
    /**
     * Mostrar elemento
     */
    static show(el) {
        if (el) el.style.display = 'block';
    }
    
    /**
     * Ocultar elemento
     */
    static hide(el) {
        if (el) el.style.display = 'none';
    }
    
    /**
     * Alternar visibilidad
     */
    static toggle(el) {
        if (el) {
            el.style.display = el.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    /**
     * Obtener valor de input
     */
    static val(el) {
        return el ? el.value : '';
    }
    
    /**
     * Establecer valor de input
     */
    static setVal(el, value) {
        if (el) el.value = value;
    }
}

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DOMUtils;
}