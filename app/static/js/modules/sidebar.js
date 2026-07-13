/**
 * MODULE: SIDEBAR
 * Maneja el toggle móvil y navegación
 */

const SidebarModule = (function() {
    'use strict';
    
    let sidebar = null;
    let toggle = null;
    let overlay = null;
    let isMobile = false;
    
    /**
     * Verifica si es dispositivo móvil
     * @returns {boolean}
     */
    function checkMobile() {
        return window.innerWidth <= 768;
    }
    
    /**
     * Toggle del sidebar
     */
    function toggleSidebar() {
        if (!isMobile) return;
        
        DOM.toggleClass(sidebar, 'open');
        DOM.toggleClass(overlay, 'active');
        
        const icon = toggle.querySelector('i');
        if (sidebar.classList.contains('open')) {
            icon.className = 'fas fa-times';
            document.body.style.overflow = 'hidden';
        } else {
            icon.className = 'fas fa-bars';
            document.body.style.overflow = '';
        }
    }
    
    /**
     * Cierra el sidebar
     */
    function closeSidebar() {
        if (!isMobile) return;
        
        DOM.removeClass(sidebar, 'open');
        DOM.removeClass(overlay, 'active');
        if (toggle) {
            toggle.querySelector('i').className = 'fas fa-bars';
        }
        document.body.style.overflow = '';
    }
    
    /**
     * Inicializa el módulo
     */
    function init() {
        sidebar = document.getElementById('sidebar');
        toggle = document.getElementById('sidebarToggle');
        overlay = document.getElementById('sidebarOverlay');
        
        if (!sidebar) {
            console.warn('Sidebar: Elemento #sidebar no encontrado');
            return;
        }
        
        isMobile = checkMobile();
        
        // Evento toggle
        if (toggle) {
            DOM.on(toggle, 'click', toggleSidebar);
        }
        
        // Evento overlay
        if (overlay) {
            DOM.on(overlay, 'click', toggleSidebar);
        }
        
        // Cerrar al hacer clic en un enlace (móvil)
        document.querySelectorAll('.sidebar a').forEach(link => {
            DOM.on(link, 'click', function() {
                if (isMobile && sidebar.classList.contains('open')) {
                    toggleSidebar();
                }
            });
        });
        
        // Cerrar al redimensionar a escritorio
        window.addEventListener('resize', function() {
            const wasMobile = isMobile;
            isMobile = checkMobile();
            
            if (!isMobile && sidebar.classList.contains('open')) {
                closeSidebar();
            }
            
            // Mostrar/ocultar toggle
            if (toggle) {
                toggle.style.display = isMobile ? 'flex' : 'none';
            }
        });
        
        // Ocultar toggle en escritorio
        if (toggle) {
            toggle.style.display = isMobile ? 'flex' : 'none';
        }
        
        console.log('✅ Sidebar module initialized');
    }
    
    // API pública
    return {
        init: init,
        toggle: toggleSidebar,
        close: closeSidebar,
    };
})();

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', SidebarModule.init);