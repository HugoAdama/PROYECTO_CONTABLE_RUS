/**
 * Sistema de Temas - Automático con notificaciones claras
 */

(function() {
    "use strict";

    const THEME_KEY = "rus-theme";
    const COLOR_KEY = "rus-primary-color";
    const DEFAULT_THEME = "dark";
    const DEFAULT_COLOR = "#60a5fa";

    function getTheme() {
        return localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
    }

    function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem(THEME_KEY, theme);
        
        // Sincronizar toggles
        document.querySelectorAll('[data-theme-toggle], #themeToggle, #modoOscuro').forEach(function(toggle) {
            if (toggle) toggle.checked = theme === "dark";
        });

        // Notificación clara
        const icon = theme === "dark" ? "🌙" : "☀️";
        const message = theme === "dark" ? "Modo oscuro activado" : "Modo claro activado";
        
        if (window.Notifications) {
            window.Notifications.info(`${icon} ${message}`);
        } else {
            console.log(`${icon} ${message}`);
        }
    }

    function toggleTheme() {
        const current = getTheme();
        setTheme(current === "dark" ? "light" : "dark");
    }

    // ============================================
    // COLOR PRIMARIO - AUTOMÁTICO CON NOTIFICACIÓN
    // ============================================

    function setPrimaryColor(color) {
        document.documentElement.style.setProperty("--color-primary", color);
        localStorage.setItem(COLOR_KEY, color);
        
        // Actualizar hex
        const hex = document.getElementById("colorHex");
        if (hex) hex.textContent = color;
        
        // Notificación clara
        if (window.Notifications) {
            window.Notifications.info(`🎨 Color actualizado: ${color}`);
        } else {
            console.log(`🎨 Color actualizado: ${color}`);
        }
    }

    function getPrimaryColor() {
        return localStorage.getItem(COLOR_KEY) || DEFAULT_COLOR;
    }

    function setupColorPicker() {
        const picker = document.getElementById("colorPrimario");
        if (picker) {
            const savedColor = getPrimaryColor();
            picker.value = savedColor;
            setPrimaryColor(savedColor);
            
            picker.removeEventListener("input", handleColorChange);
            picker.addEventListener("input", handleColorChange);
        }
    }

    function handleColorChange(event) {
        const color = event.target.value;
        setPrimaryColor(color);
    }

    // ============================================
    // TOGGLES
    // ============================================

    function setupToggles() {
        document.querySelectorAll('[data-theme-toggle], #themeToggle, #modoOscuro').forEach(function(toggle) {
            const theme = getTheme();
            toggle.checked = theme === "dark";
            toggle.removeEventListener("change", handleToggleChange);
            toggle.addEventListener("change", handleToggleChange);
        });
    }

    function handleToggleChange(event) {
        setTheme(event.target.checked ? "dark" : "light");
    }

    // ============================================
    // INICIALIZAR
    // ============================================

    function init() {
        setTheme(getTheme());
        setupToggles();
        setupColorPicker();
        console.log(`🌓 Tema: ${getTheme()}`);
        console.log(`🎨 Color: ${getPrimaryColor()}`);
    }

    // ============================================
    // EXPORTAR
    // ============================================

    window.Theme = {
        get: getTheme,
        set: setTheme,
        toggle: toggleTheme,
        setPrimaryColor: setPrimaryColor,
        getPrimaryColor: getPrimaryColor,
        init: init
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

})();
