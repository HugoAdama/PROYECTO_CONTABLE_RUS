/**
 * UTILIDADES DOM
 * Funciones helper para manipulación del DOM
 */

const DOM = {
    /**
     * Selecciona un elemento del DOM
     * @param {string} selector - Selector CSS
     * @param {HTMLElement} context - Contexto de búsqueda
     * @returns {HTMLElement|null}
     */
    el: (selector, context = document) => context.querySelector(selector),
    
    /**
     * Selecciona múltiples elementos del DOM
     * @param {string} selector - Selector CSS
     * @param {HTMLElement} context - Contexto de búsqueda
     * @returns {NodeList}
     */
    els: (selector, context = document) => context.querySelectorAll(selector),
    
    /**
     * Crea un elemento HTML
     * @param {string} tag - Etiqueta HTML
     * @param {Object} attrs - Atributos del elemento
     * @param {string|HTMLElement} content - Contenido
     * @returns {HTMLElement}
     */
    create: (tag, attrs = {}, content = '') => {
        const el = document.createElement(tag);
        Object.keys(attrs).forEach(key => {
            if (key === 'className') {
                el.className = attrs[key];
            } else if (key === 'dataset') {
                Object.keys(attrs[key]).forEach(k => {
                    el.dataset[k] = attrs[key][k];
                });
            } else {
                el.setAttribute(key, attrs[key]);
            }
        });
        if (content) {
            el.innerHTML = content;
        }
        return el;
    },
    
    /**
     * Agrega una clase a un elemento con animación
     * @param {HTMLElement} el - Elemento
     * @param {string} className - Clase a agregar
     */
    addClass: (el, className) => {
        if (el) el.classList.add(className);
    },
    
    /**
     * Remueve una clase de un elemento
     * @param {HTMLElement} el - Elemento
     * @param {string} className - Clase a remover
     */
    removeClass: (el, className) => {
        if (el) el.classList.remove(className);
    },
    
    /**
     * Toggle de clase
     * @param {HTMLElement} el - Elemento
     * @param {string} className - Clase
     */
    toggleClass: (el, className) => {
        if (el) el.classList.toggle(className);
    },
    
    /**
     * Muestra un elemento
     * @param {HTMLElement} el - Elemento
     */
    show: (el) => {
        if (el) el.style.display = '';
    },
    
    /**
     * Oculta un elemento
     * @param {HTMLElement} el - Elemento
     */
    hide: (el) => {
        if (el) el.style.display = 'none';
    },
    
    /**
     * Escucha un evento de forma segura
     * @param {HTMLElement} el - Elemento
     * @param {string} event - Nombre del evento
     * @param {Function} handler - Manejador
     */
    on: (el, event, handler) => {
        if (el) el.addEventListener(event, handler);
    },
};

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.DOM = DOM;
}