/**
 * Sistema de notificaciones para la UI
 * Proporciona toasts, alertas y barras de progreso
 */

class SistemaNotificaciones {
    constructor() {
        this.containerId = 'notificaciones-container';
        this.crearContenedor();
    }
    
    crearContenedor() {
        // Crear contenedor si no existe
        if (!document.getElementById(this.containerId)) {
            const container = document.createElement('div');
            container.id = this.containerId;
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 400px;
                width: 100%;
            `;
            document.body.appendChild(container);
        }
    }
    
    toast(tipo, mensaje, titulo = null) {
        const colores = {
            success: '#38ef7d',
            error: '#eb3349',
            warning: '#f7971e',
            info: '#4facfe'
        };
        const iconos = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        const toast = document.createElement('div');
        toast.className = 'glass-card';
        toast.style.cssText = `
            padding: 15px 20px;
            border-left: 4px solid ${colores[tipo] || '#667eea'};
            animation: slideInRight 0.3s ease;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            min-width: 280px;
        `;
        
        toast.innerHTML = `
            <span style="font-size: 1.4rem;">${iconos[tipo] || '📢'}</span>
            <div style="flex: 1;">
                ${titulo ? `<strong style="color: #fff; display: block; margin-bottom: 2px;">${titulo}</strong>` : ''}
                <span style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">${mensaje}</span>
            </div>
            <button onclick="this.parentElement.remove()" style="background: none; border: none; color: rgba(255,255,255,0.3); cursor: pointer; font-size: 1.2rem;">×</button>
        `;
        
        document.getElementById(this.containerId).appendChild(toast);
        
        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    }
    
    progreso(titulo, total) {
        const container = document.createElement('div');
        container.className = 'glass-card';
        container.id = 'progreso-container';
        container.style.cssText = `
            padding: 20px;
            margin: 10px 0;
        `;
        
        container.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">${titulo}</span>
                <span id="progreso-porcentaje" style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">0%</span>
            </div>
            <div style="height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden;">
                <div id="progreso-barra" style="width: 0%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 10px; transition: width 0.3s ease;"></div>
            </div>
            <div id="progreso-mensaje" style="color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 8px;">Iniciando...</div>
        `;
        
        // Insertar después del formulario de subida
        const uploadForm = document.getElementById('uploadForm');
        if (uploadForm) {
            uploadForm.parentNode.insertBefore(container, uploadForm.nextSibling);
        }
        
        return {
            actualizar: function(actual, total, mensaje) {
                const porcentaje = Math.min((actual / total) * 100, 100);
                const barra = document.getElementById('progreso-barra');
                const texto = document.getElementById('progreso-porcentaje');
                const msg = document.getElementById('progreso-mensaje');
                
                if (barra) barra.style.width = porcentaje + '%';
                if (texto) texto.textContent = Math.round(porcentaje) + '%';
                if (msg) msg.textContent = mensaje || `${actual} de ${total} procesados`;
            },
            completar: function(mensaje) {
                const barra = document.getElementById('progreso-barra');
                const msg = document.getElementById('progreso-mensaje');
                
                if (barra) {
                    barra.style.width = '100%';
                    barra.style.background = 'linear-gradient(90deg, #38ef7d, #11998e)';
                }
                if (msg) msg.textContent = mensaje || '✅ Proceso completado';
                
                setTimeout(() => {
                    const el = document.getElementById('progreso-container');
                    if (el) {
                        el.style.animation = 'slideOutRight 0.3s ease';
                        setTimeout(() => el.remove(), 300);
                    }
                }, 3000);
            }
        };
    }
}

// Estilos CSS para las animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Inicializar el sistema de notificaciones
const notificaciones = new SistemaNotificaciones();

// Exponer globalmente para uso en otros scripts
window.notificaciones = notificaciones;