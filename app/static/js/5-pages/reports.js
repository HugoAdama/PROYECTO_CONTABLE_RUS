/**
 * PAGES: REPORTES
 * Sistema de Control Financiero RUS v3.9.1
 * 
 * Inicializa los componentes específicos de reportes
 */

class ReportsPage {
    constructor() {
        this.init();
    }
    
    init() {
        console.log('📊 Reportes inicializado');
        this.setupExportButton();
        this.setupFilters();
    }
    
    /**
     * Configurar botón de exportación
     */
    setupExportButton() {
        const btnExport = document.getElementById('btnExportarExcel');
        if (btnExport) {
            btnExport.addEventListener('click', (e) => {
                // El enlace ya maneja la descarga
                console.log('📤 Exportando a Excel...');
            });
        }
    }
    
    /**
     * Configurar filtros de reportes
     */
    setupFilters() {
        const filtroAnio = document.getElementById('filtro-anio');
        const filtroMes = document.getElementById('filtro-mes');
        
        if (filtroAnio) {
            filtroAnio.addEventListener('change', () => {
                this.applyFilters();
            });
        }
        
        if (filtroMes) {
            filtroMes.addEventListener('change', () => {
                this.applyFilters();
            });
        }
    }
    
    /**
     * Aplicar filtros
     */
    applyFilters() {
        // Los filtros se aplican mediante el formulario
        // Este método es un placeholder para futuras extensiones
        console.log('🔍 Filtros aplicados');
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new ReportsPage();
});