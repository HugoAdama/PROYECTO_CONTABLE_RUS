/**
 * MODULES: PAGINACIÓN
 * Sistema de Control Financiero RUS v3.9.1
 */

class PaginationModule {
    constructor() {
        this.init();
    }
    
    init() {
        console.log('📄 Paginación inicializada');
        this.setupPagination();
    }
    
    /**
     * Configurar paginación
     */
    setupPagination() {
        const pagination = document.querySelector('.paginacion-verdatos');
        if (!pagination) return;
        
        const buttons = pagination.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // La navegación se maneja mediante enlaces
                // Este método es un placeholder
                console.log('📄 Página cambiada');
            });
        });
    }
    
    /**
     * Actualizar estado de paginación
     */
    update(currentPage, totalPages) {
        const pagination = document.querySelector('.paginacion-verdatos');
        if (!pagination) return;
        
        const pageText = pagination.querySelector('[style*="color:var(--text-secondary)"]');
        if (pageText) {
            pageText.textContent = `Página ${currentPage} de ${totalPages}`;
        }
        
        const prevBtn = pagination.querySelector('.btn-secondary:first-child');
        const nextBtn = pagination.querySelector('.btn-primary:last-child');
        
        if (prevBtn) {
            prevBtn.disabled = currentPage <= 1;
        }
        if (nextBtn) {
            nextBtn.disabled = currentPage >= totalPages;
        }
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new PaginationModule();
});