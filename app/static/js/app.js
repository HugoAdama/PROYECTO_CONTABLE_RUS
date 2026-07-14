/**
 * APP.JS - PUNTO DE ENTRADA PRINCIPAL
 * Sistema de Control Financiero RUS v3.9.1
 * 
 * 🏗️ ARQUITECTURA ATOMICA:
 * 1. Core - Configuración y eventos
 * 2. Utils - Utilidades
 * 3. Services - Servicios
 * 4. Modules - Módulos funcionales
 * 5. Pages - Páginas específicas
 * 
 * NOTA: Los módulos se auto-inicializan al cargar sus archivos
 */

// ============================================
// 1. CORE
// ============================================
// config.js - Configuración global
// events.js - Sistema de eventos

// ============================================
// 2. UTILS
// ============================================
// dom.js - Manipulación DOM
// format.js - Formateadores
// api.js - Cliente API
// storage.js - LocalStorage
// validators.js - Validadores

// ============================================
// 3. SERVICES
// ============================================
// theme.js - Sistema de temas
// notifications.js - Notificaciones
// auth.js - Autenticación (placeholder)

// ============================================
// 4. MODULES
// ============================================
// sidebar.js - Menú lateral
// filters.js - Filtros
// pagination.js - Paginación
// upload.js - Subida de archivos
// organizers.js - Organización de carpetas
// charts.js - Gráficos (solo en reportes)

// ============================================
// 5. PAGES
// ============================================
// dashboard.js - Dashboard
// reports.js - Reportes
// config.js - Configuración

// ============================================
// INICIALIZACIÓN PRINCIPAL
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Sistema RUS v3.9.1 iniciado');
    console.log('📐 Arquitectura: Atómica');
    console.log('✅ Todos los módulos cargados correctamente');
    
    // Verificar que los servicios globales estén disponibles
    if (window.mostrarNotificacion) {
        console.log('🔔 Sistema de notificaciones disponible');
    }
    
    // Verificar tema actual
    const isLightMode = document.body.classList.contains('light-mode');
    console.log(`🎨 Tema: ${isLightMode ? 'Claro ☀️' : 'Oscuro 🌙'}`);
});

// ============================================
// MANEJADOR DE ERRORES GLOBAL
// ============================================

window.addEventListener('error', (event) => {
    console.error('❌ Error global:', event.error || event.message);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('❌ Promesa rechazada:', event.reason);
});