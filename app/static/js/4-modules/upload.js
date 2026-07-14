/**
 * MODULES: UPLOAD
 * Sistema de Control Financiero RUS v3.9.1
 * 
 * Maneja la subida de archivos con Drag & Drop
 */

class UploadModule {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.fileList = document.getElementById('fileList');
        this.btnSubir = document.getElementById('btnSubir');
        this.btnLimpiar = document.getElementById('btnLimpiar');
        this.progressBar = document.getElementById('progressBar');
        this.uploadProgress = document.getElementById('uploadProgress');
        this.selectedFiles = [];
        this.init();
    }
    
    init() {
        console.log('📤 Upload inicializado');
        this.setupClick();
        this.setupDragDrop();
        this.setupButtons();
    }
    
    /**
     * Configurar click para seleccionar archivos
     */
    setupClick() {
        if (this.uploadArea) {
            this.uploadArea.addEventListener('click', () => {
                this.fileInput?.click();
            });
        }
        
        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => {
                this.handleFiles(e.target.files);
                this.fileInput.value = '';
            });
        }
    }
    
    /**
     * Configurar Drag & Drop
     */
    setupDragDrop() {
        if (!this.uploadArea) return;
        
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            this.handleFiles(e.dataTransfer.files);
        });
    }
    
    /**
     * Manejar archivos seleccionados
     */
    handleFiles(files) {
        const validFiles = Array.from(files).filter(f => 
            f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf')
        );
        
        if (validFiles.length === 0) {
            if (window.mostrarNotificacion) {
                window.mostrarNotificacion('⚠️ Solo se permiten archivos PDF', 'warning');
            }
            return;
        }
        
        this.selectedFiles = [...this.selectedFiles, ...validFiles];
        this.renderFileList();
        this.updateButtons();
        
        if (window.mostrarNotificacion) {
            window.mostrarNotificacion(`✅ ${validFiles.length} archivo(s) seleccionado(s)`, 'success');
        }
    }
    
    /**
     * Renderizar lista de archivos
     */
    renderFileList() {
        if (!this.fileList) return;
        
        if (this.selectedFiles.length === 0) {
            this.fileList.innerHTML = '';
            return;
        }
        
        this.fileList.innerHTML = this.selectedFiles.map((file, index) => `
            <div class="file-item" data-index="${index}">
                <span class="file-icon">📄</span>
                <span class="file-name">${file.name}</span>
                <span class="file-size">${(file.size / 1024).toFixed(1)} KB</span>
                <span class="file-status pending">⏳</span>
                <button class="btn btn-sm btn-danger" onclick="window.removeFile(${index})" style="padding:4px 10px; font-size:0.8rem;">
                    ✕
                </button>
            </div>
        `).join('');
        
        // Exponer función de eliminación
        window.removeFile = (index) => {
            this.selectedFiles.splice(index, 1);
            this.renderFileList();
            this.updateButtons();
        };
    }
    
    /**
     * Configurar botones
     */
    setupButtons() {
        if (this.btnSubir) {
            this.btnSubir.addEventListener('click', () => {
                this.uploadFiles();
            });
        }
        
        if (this.btnLimpiar) {
            this.btnLimpiar.addEventListener('click', () => {
                this.selectedFiles = [];
                this.renderFileList();
                this.updateButtons();
                this.uploadProgress?.classList.remove('active');
                if (this.progressBar) this.progressBar.style.width = '0%';
            });
        }
    }
    
    /**
     * Actualizar estado de botones
     */
    updateButtons() {
        const hasFiles = this.selectedFiles.length > 0;
        if (this.btnSubir) this.btnSubir.disabled = !hasFiles;
        if (this.btnLimpiar) this.btnLimpiar.disabled = !hasFiles;
    }
    
    /**
     * Subir archivos
     */
    uploadFiles() {
        if (this.selectedFiles.length === 0) return;
        
        if (this.btnSubir) {
            this.btnSubir.disabled = true;
            this.btnSubir.innerHTML = '⏳ Subiendo...';
        }
        
        if (this.uploadProgress) {
            this.uploadProgress.classList.add('active');
        }
        
        // Simular progreso
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress <= 90 && this.progressBar) {
                this.progressBar.style.width = progress + '%';
            }
        }, 200);
        
        // Simular subida
        setTimeout(() => {
            clearInterval(interval);
            if (this.progressBar) this.progressBar.style.width = '100%';
            
            // Marcar archivos como procesados
            this.fileList?.querySelectorAll('.file-item .file-status').forEach(el => {
                el.textContent = '✅';
                el.className = 'file-status success';
            });
            
            if (this.btnSubir) {
                this.btnSubir.innerHTML = '✅ Completado';
            }
            
            if (window.mostrarNotificacion) {
                window.mostrarNotificacion('✅ Archivos subidos y procesados correctamente', 'success');
            }
            
            setTimeout(() => {
                if (this.btnSubir) {
                    this.btnSubir.disabled = false;
                    this.btnSubir.innerHTML = '🚀 Subir y Procesar';
                }
                if (this.uploadProgress) {
                    this.uploadProgress.classList.remove('active');
                }
                if (this.progressBar) this.progressBar.style.width = '0%';
                this.selectedFiles = [];
                this.renderFileList();
                this.updateButtons();
            }, 2000);
            
        }, 3000);
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new UploadModule();
});