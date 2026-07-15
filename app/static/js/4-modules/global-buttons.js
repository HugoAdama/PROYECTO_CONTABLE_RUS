/**
 * Botones globales - Restablecer y Limpiar Caché
 */

(function() {
    "use strict";

    // ============================================
    // RESTABLECER CONFIGURACIÓN
    // ============================================

    function resetConfig() {
        if (confirm('⚠️ ¿Estás seguro de restablecer toda la configuración? Esta acción es irreversible.')) {
            try {
                // Limpiar localStorage
                localStorage.clear();
                
                // Mostrar notificación de éxito
                if (window.Notifications) {
                    window.Notifications.success('🔄 Configuración restablecida correctamente');
                }
                
                // Recargar después de 1.5 segundos
                setTimeout(function() {
                    location.reload();
                }, 1500);
                
            } catch (error) {
                if (window.Notifications) {
                    window.Notifications.error('❌ Error al restablecer configuración');
                }
                console.error('Error resetting config:', error);
            }
        }
    }

    // ============================================
    // LIMPIAR CACHÉ
    // ============================================

    function clearCache() {
        if (confirm('🗑️ ¿Limpiar caché del navegador? Se recargará la página.')) {
            try {
                // Limpiar caché del navegador
                if ('caches' in window) {
                    caches.keys().then(function(names) {
                        names.forEach(function(name) {
                            caches.delete(name);
                        });
                    });
                }
                
                // Mostrar notificación de éxito
                if (window.Notifications) {
                    window.Notifications.success('🗑️ Caché limpiado correctamente');
                }
                
                // Recargar después de 1.5 segundos
                setTimeout(function() {
                    location.reload();
                }, 1500);
                
            } catch (error) {
                if (window.Notifications) {
                    window.Notifications.error('❌ Error al limpiar caché');
                }
                console.error('Error clearing cache:', error);
            }
        }
    }

    // ============================================
    // CONFIGURAR BOTONES EN LA PÁGINA
    // ============================================

    function setupButtons() {
        // Botón Restablecer
        const resetBtn = document.getElementById('btnResetearConfig');
        if (resetBtn) {
            resetBtn.removeEventListener('click', resetConfig);
            resetBtn.addEventListener('click', resetConfig);
        }

        // Botón Limpiar Caché
        const cacheBtn = document.getElementById('btnLimpiarCache');
        if (cacheBtn) {
            cacheBtn.removeEventListener('click', clearCache);
            cacheBtn.addEventListener('click', clearCache);
        }
    }

    // ============================================
    // INICIALIZAR
    // ============================================

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", setupButtons);
    } else {
        setupButtons();
    }

    // Escuchar cambios en el DOM (para páginas con carga dinámica)
    const observer = new MutationObserver(function() {
        setupButtons();
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

})();
