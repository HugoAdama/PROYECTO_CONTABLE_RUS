/**
 * MODULES: SIDEBAR
 * Sistema de Control Financiero RUS v3.9.1
 * 
 * Maneja el toggle del menú lateral en móviles
 */

class SidebarModule {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.toggle = document.getElementById('sidebarToggle');
        this.overlay = document.getElementById('sidebarOverlay');
        this.init();
    }
    
    init() {
        console.log('📱 Sidebar inicializado');
        this.setupToggle();
        this.setupResize();
        this.setupLinks();
    }
    
    /**
     * Configurar toggle
     */
    setupToggle() {
        if (!this.sidebar || !this.toggle) return;
        
        this.toggle.addEventListener('click', () => {
            this.toggleSidebar();
        });
        
        if (this.overlay) {
            this.overlay.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }
    }
    
    /**
     * Alternar sidebar
     */
    toggleSidebar() {
        if (!this.isMobile()) return;
        
        this.sidebar.classList.toggle('open');
        if (this.overlay) this.overlay.classList.toggle('active');
        
        const icon = this.toggle.querySelector('i');
        if (icon) {
            icon.className = this.sidebar.classList.contains('open') 
                ? 'fas fa-times' 
                : 'fas fa-bars';
        }
        
        document.body.style.overflow = this.sidebar.classList.contains('open') 
            ? 'hidden' 
            : '';
    }
    
    /**
     * Verificar si es móvil
     */
    isMobile() {
        return window.innerWidth <= 768;
    }
    
    /**
     * Configurar redimensionamiento
     */
    setupResize() {
        window.addEventListener('resize', () => {
            if (!this.isMobile() && this.sidebar?.classList.contains('open')) {
                this.sidebar.classList.remove('open');
                if (this.overlay) this.overlay.classList.remove('active');
                const icon = this.toggle?.querySelector('i');
                if (icon) icon.className = 'fas fa-bars';
                document.body.style.overflow = '';
            }
        });
    }
    
    /**
     * Configurar enlaces
     */
    setupLinks() {
        this.sidebar?.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (this.isMobile() && this.sidebar?.classList.contains('open')) {
                    this.toggleSidebar();
                }
            });
        });
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new SidebarModule();
});