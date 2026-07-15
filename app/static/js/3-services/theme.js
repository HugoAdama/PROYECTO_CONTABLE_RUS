/**
 * Sistema de Temas - Global y persistente
 * Controla el tema en todas las páginas
 */

(function() {
    "use strict";

    const THEME_KEY = "rus-theme";
    const DEFAULT_THEME = "dark";

    // ============================================
    // OBTENER TEMA GUARDADO
    // ============================================

    function getTheme() {
        return localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
    }

    // ============================================
    // APLICAR TEMA
    // ============================================

    function setTheme(theme) {
        // Aplicar al HTML
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem(THEME_KEY, theme);

        // Sincronizar todos los toggles en la página
        const toggles = document.querySelectorAll('#themeToggle, #modoOscuro, [data-theme-toggle]');
        toggles.forEach(function(toggle) {
            if (toggle) {
                toggle.checked = theme === "dark";
            }
        });

        // Notificar cambio
        const icon = theme === "dark" ? "🌙" : "☀️";
        const message = theme === "dark" ? "Modo oscuro activado" : "Modo claro activado";
        console.log(`${icon} ${message}`);

        // Emitir evento para que otros scripts puedan reaccionar
        const event = new CustomEvent('themeChanged', { detail: { theme: theme } });
        document.dispatchEvent(event);
    }

    // ============================================
    // ALTERNAR TEMA
    // ============================================

    function toggleTheme() {
        const current = getTheme();
        const next = current === "dark" ? "light" : "dark";
        setTheme(next);
    }

    // ============================================
    // CONFIGURAR TOGGLES
    // ============================================

    function setupToggles() {
        const toggles = document.querySelectorAll('#themeToggle, #modoOscuro, [data-theme-toggle]');
        toggles.forEach(function(toggle) {
            const theme = getTheme();
            toggle.checked = theme === "dark";

            // Remover listeners anteriores para evitar duplicados
            toggle.removeEventListener("change", handleToggleChange);
            toggle.addEventListener("change", handleToggleChange);
        });
    }

    function handleToggleChange(event) {
        const toggle = event.target;
        setTheme(toggle.checked ? "dark" : "light");
    }

    // ============================================
    // INICIALIZAR
    // ============================================

    function init() {
        const theme = getTheme();
        setTheme(theme);
        setupToggles();
        console.log(`🌓 Tema: ${theme}`);
    }

    // ============================================
    // EXPORTAR
    // ============================================

    window.Theme = {
        get: getTheme,
        set: setTheme,
        toggle: toggleTheme,
        init: init,
        setupToggles: setupToggles
    };

    // ============================================
    // EJECUTAR
    // ============================================

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

    // ============================================
    // OBSERVAR CAMBIOS EN EL DOM
    // ============================================

    const observer = new MutationObserver(function() {
        setupToggles();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

})();
