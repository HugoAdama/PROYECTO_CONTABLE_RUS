/**
 * UTILS: CLIENTE API
 * Sistema de Control Financiero RUS v3.9.1
 */

class ApiClient {
    constructor() {
        this.baseUrl = '';
        this.headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        };
    }
    
    /**
     * Petición GET
     */
    async get(endpoint, params = {}) {
        const url = this.buildUrl(endpoint, params);
        const response = await fetch(url, {
            method: 'GET',
            headers: this.headers,
        });
        return this.handleResponse(response);
    }
    
    /**
     * Petición POST
     */
    async post(endpoint, data = {}) {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data),
        });
        return this.handleResponse(response);
    }
    
    /**
     * Petición PUT
     */
    async put(endpoint, data = {}) {
        const response = await fetch(endpoint, {
            method: 'PUT',
            headers: this.headers,
            body: JSON.stringify(data),
        });
        return this.handleResponse(response);
    }
    
    /**
     * Petición DELETE
     */
    async delete(endpoint) {
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: this.headers,
        });
        return this.handleResponse(response);
    }
    
    /**
     * Construir URL con parámetros
     */
    buildUrl(endpoint, params) {
        const url = new URL(endpoint, window.location.origin);
        Object.keys(params).forEach(key => {
            if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
                url.searchParams.append(key, params[key]);
            }
        });
        return url.toString();
    }
    
    /**
     * Manejar respuesta
     */
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || `Error ${response.status}: ${response.statusText}`);
        }
        return response.json();
    }
    
    /**
     * Configurar token de autenticación (para futuro)
     */
    setAuthToken(token) {
        if (token) {
            this.headers['Authorization'] = `Bearer ${token}`;
        } else {
            delete this.headers['Authorization'];
        }
    }
}

// ============================================
// INSTANCIA GLOBAL
// ============================================
const api = new ApiClient();

// ============================================
// EXPORTAR
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
}