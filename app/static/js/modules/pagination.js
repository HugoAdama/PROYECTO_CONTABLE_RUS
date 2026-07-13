/**
 * MODULE: PAGINATION
 * Maneja la paginación de tablas
 */

const PaginationModule = (function() {
    'use strict';
    
    /**
     * Cambia a una página específica
     * @param {number} page - Número de página
     * @param {string} paramName - Nombre del parámetro (default: 'page')
     */
    function goToPage(page, paramName = 'page') {
        const url = new URL(window.location.href);
        url.searchParams.set(paramName, page);
        window.location.href = url.toString();
    }
    
    /**
     * Cambia el número de elementos por página
     * @param {number} perPage - Elementos por página
     * @param {string} paramName - Nombre del parámetro (default: 'per_page')
     */
    function setPerPage(perPage, paramName = 'per_page') {
        const url = new URL(window.location.href);
        url.searchParams.set(paramName, perPage);
        url.searchParams.delete('page'); // Resetear página
        window.location.href = url.toString();
    }
    
    /**
     * Obtiene el número de página actual
     * @param {string} paramName - Nombre del parámetro (default: 'page')
     * @param {number} defaultPage - Página por defecto
     * @returns {number}
     */
    function getCurrentPage(paramName = 'page', defaultPage = 1) {
        const url = new URL(window.location.href);
        const page = parseInt(url.searchParams.get(paramName));
        return isNaN(page) || page < 1 ? defaultPage : page;
    }
    
    /**
     * Obtiene el número de elementos por página actual
     * @param {string} paramName - Nombre del parámetro (default: 'per_page')
     * @param {number} defaultPerPage - Valor por defecto
     * @returns {number}
     */
    function getPerPage(paramName = 'per_page', defaultPerPage = 10) {
        const url = new URL(window.location.href);
        const perPage = parseInt(url.searchParams.get(paramName));
        return isNaN(perPage) || perPage < 1 ? defaultPerPage : perPage;
    }
    
    // API pública
    return {
        goToPage: goToPage,
        setPerPage: setPerPage,
        getCurrentPage: getCurrentPage,
        getPerPage: getPerPage,
    };
})();

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.PaginationModule = PaginationModule;
    window.cambiarPagina = PaginationModule.goToPage;
}