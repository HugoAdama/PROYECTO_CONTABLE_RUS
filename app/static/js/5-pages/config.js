/**
 * PAGES: CONFIGURACIÓN
 * Sistema de Control Financiero RUS v3.9.1
 */

import { Validators } from '../2-utils/validators.js';
import { notifications } from '../3-services/notifications.js';
import { themeService } from '../3-services/theme.js';

class ConfigPage {
    constructor() {
        this.form = document.getElementById('formConfigGeneral');
        this.btnGuardarGeneral = document.getElementById('btnGuardarGeneral');
        this.feedbackGeneral = document.getElementById('feedbackGeneral');
        this.emailInput = document.getElementById('emailNotificaciones');
        this.emailError = document.getElementById('emailError');
        this.init();
    }
    
    init() {
        this.setupGeneralForm();
        this.setupRealTimeValidation();
        this.setupResetButton();
        this.setupClearCacheButton();
    }
    
    setupGeneralForm() {
        if (!this.form) return;
        
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const email = this.emailInput.value.trim();
            
            if (!Validators.isEmail(email)) {
                this.emailInput.classList.add('error');
                this.emailError.classList.add('show');
                return;
            }
            
            this.emailInput.classList.remove('error');
            this.emailError.classList.remove('show');
            
            const nombre = document.getElementById('nombreNegocio')?.value.trim() || '';
            const notificaciones = document.getElementById('notificacionesActivas')?.checked || false;
            
            this.btnGuardarGeneral.innerHTML = '⏳ Guardando...';
            this.btnGuardarGeneral.disabled = true;
            
            // Simular guardado
            setTimeout(() => {
                this.btnGuardarGeneral.innerHTML = '💾 Guardar Cambios';
                this.btnGuardarGeneral.disabled = false;
                
                this.feedbackGeneral.className = 'save-feedback success';
                this.feedbackGeneral.innerHTML = '✅ Configuración guardada correctamente';
                
                setTimeout(() => {
                    this.feedbackGeneral.className = 'save-feedback';
                    this.feedbackGeneral.innerHTML = '';
                }, 4000);
                
                notifications.success('✅ Configuración guardada correctamente');
            }, 1200);
        });
    }
    
    setupRealTimeValidation() {
        if (!this.emailInput) return;
        
        this.emailInput.addEventListener('input', () => {
            const email = this.emailInput.value.trim();
            
            if (email && !Validators.isEmail(email)) {
                this.emailInput.classList.add('error');
                this.emailError.classList.add('show');
            } else {
                this.emailInput.classList.remove('error');
                this.emailError.classList.remove('show');
            }
        });
    }
    
    setupResetButton() {
        const btnReset = document.getElementById('btnResetearConfig');
        if (!btnReset) return;
        
        btnReset.addEventListener('click', () => {
            if (confirm('⚠️ ¿Estás seguro de restablecer toda la configuración?')) {
                notifications.info('🔄 Restableciendo configuración...');
                
                document.getElementById('nombreNegocio').value = 'Mi Negocio';
                document.getElementById('emailNotificaciones').value = 'negocio@email.com';
                document.getElementById('notificacionesActivas').checked = true;
                document.getElementById('modoOscuro').checked = true;
                document.getElementById('colorPrimario').value = '#60a5fa';
                document.getElementById('colorHex').textContent = '#60a5fa';
                
                storage.clear();
                
                setTimeout(() => {
                    notifications.success('✅ Configuración restablecida');
                    location.reload();
                }, 1000);
            }
        });
    }
    
    setupClearCacheButton() {
        const btnClear = document.getElementById('btnLimpiarCache');
        if (!btnClear) return;
        
        btnClear.addEventListener('click', () => {
            if (confirm('🗑️ ¿Limpiar caché del sistema?')) {
                notifications.info('🗑️ Limpiando caché...');
                localStorage.clear();
                sessionStorage.clear();
                setTimeout(() => {
                    notifications.success('✅ Caché limpiada correctamente');
                }, 1000);
            }
        });
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new ConfigPage();
});