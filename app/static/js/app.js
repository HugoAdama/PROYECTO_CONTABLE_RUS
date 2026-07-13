/**
 * APP.JS - PUNTO DE ENTRADA PRINCIPAL
 * Inicializa todos los módulos de la aplicación
 */

(function() {
    'use strict';
    
    console.log('🚀 Inicializando aplicación...');
    
    // ============================================
    // INICIALIZAR MÓDULOS
    // ============================================
    
    // 1. Sidebar (siempre necesario)
    if (typeof SidebarModule !== 'undefined' && SidebarModule.init) {
        SidebarModule.init();
        console.log('✅ Sidebar module initialized');
    }
    
    // 2. Notificaciones (siempre disponible)
    if (typeof NotificationsModule !== 'undefined') {
        console.log('✅ Notifications module ready');
    }
    
    // 3. Upload (si existe drop zone)
    if (typeof UploadModule !== 'undefined' && document.getElementById('drop-zone')) {
        UploadModule.init();
        console.log('✅ Upload module initialized');
    }
    
    // 4. Charts (si existe Plotly)
    if (typeof Plotly !== 'undefined' && typeof ChartsModule !== 'undefined') {
        console.log('✅ Charts module ready');
    }
    
    // 5. Filtros (si existen)
    if (typeof FiltersModule !== 'undefined') {
        console.log('✅ Filters module ready');
    }
    
    // 6. Paginación (si existe)
    if (typeof PaginationModule !== 'undefined') {
        console.log('✅ Pagination module ready');
    }
    
    console.log('✅ Aplicación inicializada correctamente');
    
})();