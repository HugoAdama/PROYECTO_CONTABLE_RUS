/**
 * UTILIDADES API
 * Funciones para peticiones fetch
 */

const API = {
    /**
     * Realiza una petición GET
     * @param {string} url - URL del endpoint
     * @param {Object} params - Parámetros query string
     * @returns {Promise}
     */
    get: async (url, params = {}) => {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        
        try {
            const response = await fetch(fullUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET error:', error);
            throw error;
        }
    },
    
    /**
     * Realiza una petición POST
     * @param {string} url - URL del endpoint
     * @param {Object} data - Datos a enviar
     * @returns {Promise}
     */
    post: async (url, data = {}) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API POST error:', error);
            throw error;
        }
    },
    
    /**
     * Realiza una petición con FormData (para archivos)
     * @param {string} url - URL del endpoint
     * @param {FormData} formData - Datos del formulario
     * @returns {Promise}
     */
    upload: async (url, formData) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API UPLOAD error:', error);
            throw error;
        }
    },
    
    /**
     * Descarga un archivo
     * @param {string} url - URL del archivo
     * @param {Object} params - Parámetros
     * @param {string} filename - Nombre del archivo
     */
    download: async (url, params = {}, filename = 'download') => {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        
        try {
            const response = await fetch(fullUrl);
            const blob = await response.blob();
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(link.href);
        } catch (error) {
            console.error('Download error:', error);
            throw error;
        }
    },
};

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.API = API;
}