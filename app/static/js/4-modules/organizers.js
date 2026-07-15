/**
 * MODULES: ORGANIZACIÓN DE CARPETAS
 * Sistema de Control Financiero RUS v3.9.1
 */

import { APP_CONFIG } from '../1-core/config.js';
import { notifications } from '../3-services/notifications.js';

class OrganizersModule {
    constructor() {
        this.btnOrganizar = document.getElementById('btnOrganizar');
        this.btnEstadisticas = document.getElementById('btnEstadisticas');
        this.init();
    }
    
    init() {
        this.setupOrganizar();
        this.setupEstadisticas();
        this.setupLegacySupport();
    }
    
    setupOrganizar() {
        if (!this.btnOrganizar) return;
        
        this.btnOrganizar.addEventListener('click', async () => {
            const originalText = this.btnOrganizar.innerHTML;
            const originalDisabled = this.btnOrganizar.disabled;
            
            this.btnOrganizar.innerHTML = '⏳ Organizando...';
            this.btnOrganizar.disabled = true;
            this.btnOrganizar.style.opacity = '0.7';
            
            notifications.info('🔄 Organizando carpetas automáticamente...');
            
            try {
                const response = await fetch(APP_CONFIG.API.ORGANIZAR_CARPETAS, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });
                
                const data = await response.json();
                
                this.btnOrganizar.innerHTML = originalText;
                this.btnOrganizar.disabled = false;
                this.btnOrganizar.style.opacity = '1';
                
                if (data.success) {
                    notifications.success('✅ Carpetas organizadas correctamente');
                    setTimeout(() => location.reload(), 1500);
                } else {
                    notifications.error('❌ Error: ' + (data.message || 'Error desconocido'));
                }
            } catch (error) {
                this.btnOrganizar.innerHTML = originalText;
                this.btnOrganizar.disabled = false;
                this.btnOrganizar.style.opacity = '1';
                notifications.error('❌ Error al conectar con el servidor');
            }
        });
    }
    
    setupEstadisticas() {
        if (!this.btnEstadisticas) return;
        
        this.btnEstadisticas.addEventListener('click', () => {
            notifications.info('📊 Cargando estadísticas...');
            window.location.href = '/reportes';
        });
    }
    
    setupLegacySupport() {
        window.organizarAutomatico = () => this.btnOrganizar?.click();
        window.verEstadisticas = () => this.btnEstadisticas?.click();
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new OrganizersModule();
});