/**
 * MODULES: FILTERS
 * Sistema de Control Financiero RUS v3.9.1
 * 
 * Maneja los filtros de la página de datos
 */

class FiltersModule {
    constructor() {
        this.init();
    }
    
    init() {
        console.log('🔍 Filtros inicializados');
        this.setupFilters();
        this.setupClearButton();
    }
    
    /**
     * Configurar filtros
     */
    setupFilters() {
        const form = document.querySelector('.filtros-verdatos');
        if (!form) return;
        
        form.addEventListener('submit', (e) => {
            // El formulario se envía normalmente
            // Este método es un placeholder para futuras extensiones
            console.log('🔍 Filtros aplicados');
        });
    }
    
    /**
     * Configurar botón de limpiar
     */
    setupClearButton() {
        const btnLimpiar = document.querySelector('.filtros-verdatos .btn-secondary');
        if (!btnLimpiar) return;
        
        btnLimpiar.addEventListener('click', () => {
            const selects = document.querySelectorAll('.filtros-verdatos select');
            selects.forEach(select => {
                select.selectedIndex = 0;
            });
            console.log('🗑️ Filtros limpiados');
        });
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new FiltersModule();
});