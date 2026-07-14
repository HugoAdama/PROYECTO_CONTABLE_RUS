/**
 * SERVICES: SISTEMA DE TEMAS
 * Sistema de Control Financiero RUS v3.9.1
 */

import { APP_CONFIG } from '../1-core/config.js';
import { storage } from '../2-utils/storage.js';
import { eventBus } from '../1-core/events.js';

class ThemeService {
    constructor() {
        this.currentTheme = this.loadTheme();
        this.init();
    }
    
    /**
     * Inicializar
     */
    init() {
        this.applyTheme(this.currentTheme);
        this.setupToggle();
        this.setupColorPicker();
    }
    
    /**
     * Cargar tema desde storage
     */
    loadTheme() {
        const saved = storage.get(APP_CONFIG.STORAGE.TEMA);
        if (saved === 'light' || saved === 'dark') {
            return saved;
        }
        // Detectar preferencia del sistema
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
            return 'light';
        }
        return 'dark';
    }
    
    /**
     * Aplicar tema
     */
    applyTheme(theme) {
        this.currentTheme = theme;
        const body = document.body;
        
        if (theme === 'light') {
            body.classList.add('light-mode');
        } else {
            body.classList.remove('light-mode');
        }
        
        storage.set(APP_CONFIG.STORAGE.TEMA, theme);
        eventBus.emit('themeChanged', { theme });
        this.updateToggle();
    }
    
    /**
     * Alternar tema
     */
    toggle() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
    }
    
    /**
     * Configurar toggle
     */
    setupToggle() {
        const toggle = document.getElementById('modoOscuro');
        if (toggle) {
            toggle.addEventListener('change', () => {
                this.toggle();
                this.showNotification();
            });
        }
    }
    
    /**
     * Configurar color picker
     */
    setupColorPicker() {
        const colorInput = document.getElementById('colorPrimario');
        const colorHex = document.getElementById('colorHex');
        
        if (colorInput) {
            const savedColor = storage.get(APP_CONFIG.STORAGE.COLOR_PRIMARIO, '#60a5fa');
            colorInput.value = savedColor;
            if (colorHex) colorHex.textContent = savedColor;
            
            colorInput.addEventListener('input', () => {
                const color = colorInput.value;
                if (colorHex) colorHex.textContent = color;
                document.documentElement.style.setProperty('--color-primary', color);
                storage.set(APP_CONFIG.STORAGE.COLOR_PRIMARIO, color);
            });
        }
    }
    
    /**
     * Actualizar toggle
     */
    updateToggle() {
        const toggle = document.getElementById('modoOscuro');
        if (toggle) {
            toggle.checked = this.currentTheme === 'light';
        }
    }
    
    /**
     * Mostrar notificación
     */
    showNotification() {
        const mensaje = this.currentTheme === 'light' 
            ? '☀️ Modo claro activado' 
            : '🌙 Modo oscuro activado';
        
        if (window.mostrarNotificacion) {
            window.mostrarNotificacion(mensaje, 'info');
        }
    }
}

// ============================================
// INSTANCIA GLOBAL
// ============================================
const themeService = new ThemeService();

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = themeService;
}