/**
 * SERVICES: AUTENTICACIÓN
 * Sistema de Control Financiero RUS v3.9.1
 * 
 * NOTA: Este servicio está preparado para futura implementación
 * de autenticación de usuarios.
 */

class AuthService {
    constructor() {
        this.isAuthenticated = false;
        this.user = null;
        this.token = null;
    }
    
    /**
     * Verificar si el usuario está autenticado
     */
    checkAuth() {
        // Por ahora, siempre retorna true (modo desarrollo)
        // En el futuro, verificará el token en localStorage
        return true;
    }
    
    /**
     * Iniciar sesión
     */
    login(email, password) {
        // Implementación futura
        console.warn('⚠️ AuthService.login() - Pendiente de implementación');
        return Promise.resolve({ success: true });
    }
    
    /**
     * Cerrar sesión
     */
    logout() {
        // Implementación futura
        console.warn('⚠️ AuthService.logout() - Pendiente de implementación');
        return Promise.resolve({ success: true });
    }
    
    /**
     * Obtener usuario actual
     */
    getCurrentUser() {
        return this.user;
    }
}

// ============================================
// INSTANCIA GLOBAL
// ============================================
const authService = new AuthService();

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = authService;
}