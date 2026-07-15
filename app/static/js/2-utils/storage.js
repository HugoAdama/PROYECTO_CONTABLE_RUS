/**
 * UTILS: GESTOR DE LOCALSTORAGE
 * Sistema de Control Financiero RUS v3.9.1
 */

class StorageManager {
    constructor() {
        this.prefix = 'rus_';
    }
    
    /**
     * Guardar valor
     */
    set(key, value) {
        try {
            const fullKey = this.prefix + key;
            localStorage.setItem(fullKey, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Storage set error:', error);
            return false;
        }
    }
    
    /**
     * Obtener valor
     */
    get(key, defaultValue = null) {
        try {
            const fullKey = this.prefix + key;
            const value = localStorage.getItem(fullKey);
            return value ? JSON.parse(value) : defaultValue;
        } catch (error) {
            console.error('Storage get error:', error);
            return defaultValue;
        }
    }
    
    /**
     * Eliminar valor
     */
    remove(key) {
        try {
            const fullKey = this.prefix + key;
            localStorage.removeItem(fullKey);
            return true;
        } catch (error) {
            console.error('Storage remove error:', error);
            return false;
        }
    }
    
    /**
     * Limpiar todo
     */
    clear() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith(this.prefix)) {
                    localStorage.removeItem(key);
                }
            });
            return true;
        } catch (error) {
            console.error('Storage clear error:', error);
            return false;
        }
    }
}

// ============================================
// INSTANCIA GLOBAL
// ============================================
const storage = new StorageManager();

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = storage;
}