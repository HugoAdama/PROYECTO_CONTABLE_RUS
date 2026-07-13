/**
 * MODULE: UPLOAD
 * Maneja la subida de archivos con Drag & Drop
 */

const UploadModule = (function() {
    'use strict';
    
    let dropZone = null;
    let fileInput = null;
    
    /**
     * Inicializa el módulo de upload
     * @param {string} dropZoneId - ID del drop zone
     * @param {string} fileInputId - ID del input file
     */
    function init(dropZoneId = 'drop-zone', fileInputId = 'fileInput') {
        dropZone = document.getElementById(dropZoneId);
        fileInput = document.getElementById(fileInputId);
        
        if (!dropZone) {
            console.warn('Upload: Drop zone no encontrado');
            return;
        }
        
        setupDragDrop();
        setupClick();
    }
    
    /**
     * Configura Drag & Drop
     */
    function setupDragDrop() {
        // Prevenir comportamientos por defecto
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });
        
        // Highlight al arrastrar
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('dragover');
            });
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('dragover');
            });
        });
        
        // Drop
        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            handleFiles(files);
        });
    }
    
    /**
     * Configura clic para seleccionar archivos
     */
    function setupClick() {
        dropZone.addEventListener('click', () => {
            if (fileInput) fileInput.click();
        });
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                handleFiles(e.target.files);
                fileInput.value = ''; // Resetear
            });
        }
    }
    
    /**
     * Procesa los archivos seleccionados
     * @param {FileList} files - Lista de archivos
     */
    function handleFiles(files) {
        const validFiles = [];
        const errors = [];
        
        Array.from(files).forEach(file => {
            // Validar tipo
            if (file.type !== 'application/pdf') {
                errors.push(`${file.name} no es un PDF válido`);
                return;
            }
            
            // Validar tamaño
            const maxSize = APP_CONFIG?.UPLOAD?.MAX_FILE_SIZE || 52428800;
            if (file.size > maxSize) {
                errors.push(`${file.name} excede el tamaño máximo (50MB)`);
                return;
            }
            
            validFiles.push(file);
        });
        
        if (errors.length > 0) {
            errors.forEach(error => {
                NotificationsModule.error(error);
            });
        }
        
        if (validFiles.length > 0) {
            NotificationsModule.success(`${validFiles.length} archivo(s) seleccionado(s) correctamente`);
            onFilesSelected(validFiles);
        }
    }
    
    /**
     * Callback cuando se seleccionan archivos
     * @param {Array} files - Archivos válidos
     */
    function onFilesSelected(files) {
        // Este método puede ser sobrescrito desde fuera
        console.log('Archivos seleccionados:', files);
    }
    
    /**
     * Establece el callback para archivos seleccionados
     * @param {Function} callback - Función a ejecutar
     */
    function setOnFilesSelected(callback) {
        if (typeof callback === 'function') {
            onFilesSelected = callback;
        }
    }
    
    // API pública
    return {
        init: init,
        setOnFilesSelected: setOnFilesSelected,
    };
})();

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.UploadModule = UploadModule;
}