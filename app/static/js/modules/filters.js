/**
 * MODULE: FILTERS
 * Maneja los filtros de la página
 */

const FiltersModule = (function() {
    'use strict';
    
    /**
     * Aplica los filtros y redirige
     * @param {string} baseUrl - URL base
     * @param {Object} filters - Objeto con los filtros
     */
    function applyFilters(baseUrl, filters = {}) {
        const params = new URLSearchParams();
        
        Object.keys(filters).forEach(key => {
            const value = filters[key];
            if (value && value !== '' && value !== 'todos') {
                params.append(key, value);
            }
        });
        
        const queryString = params.toString();
        const url = queryString ? `${baseUrl}?${queryString}` : baseUrl;
        window.location.href = url;
    }
    
    /**
     * Obtiene los filtros del formulario
     * @param {string} formId - ID del formulario
     * @param {Array} fields - Nombres de los campos
     * @returns {Object}
     */
    function getFormFilters(formId, fields = []) {
        const form = document.getElementById(formId);
        if (!form) return {};
        
        const filters = {};
        fields.forEach(field => {
            const input = form.querySelector(`[name="${field}"]`);
            if (input) {
                filters[field] = input.value;
            }
        });
        
        return filters;
    }
    
    /**
     * Limpia los filtros de un formulario
     * @param {string} formId - ID del formulario
     * @param {Array} fields - Nombres de los campos
     */
    function clearFilters(formId, fields = []) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        fields.forEach(field => {
            const input = form.querySelector(`[name="${field}"]`);
            if (input) {
                input.value = '';
                if (input.tagName === 'SELECT') {
                    input.selectedIndex = 0;
                }
            }
        });
    }
    
    // API pública
    return {
        applyFilters: applyFilters,
        getFormFilters: getFormFilters,
        clearFilters: clearFilters,
    };
})();

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.FiltersModule = FiltersModule;
    window.aplicarFiltros = FiltersModule.applyFilters;
    window.limpiarFiltros = FiltersModule.clearFilters;
}