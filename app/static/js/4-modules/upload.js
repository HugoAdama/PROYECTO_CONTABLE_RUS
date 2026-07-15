/**
 * Upload - Feedback de subida de archivos
 * Mejora la experiencia al subir archivos
 */

(function() {
    "use strict";

    // ============================================
    // DRAG & DROP CON FEEDBACK VISUAL
    // ============================================

    const dropZone = document.getElementById("drop-zone");
    if (dropZone) {
        // Estado de arrastre
        let dragCounter = 0;
        
        dropZone.addEventListener("dragenter", function(e) {
            e.preventDefault();
            dragCounter++;
            if (dragCounter === 1) {
                dropZone.classList.add("drag-over");
                // Feedback visual: borde brillante
                dropZone.style.borderColor = "var(--color-primary)";
                dropZone.style.boxShadow = "0 0 30px rgba(96, 165, 250, 0.2)";
            }
        });
        
        dropZone.addEventListener("dragleave", function(e) {
            e.preventDefault();
            dragCounter--;
            if (dragCounter === 0) {
                dropZone.classList.remove("drag-over");
                dropZone.style.borderColor = "";
                dropZone.style.boxShadow = "";
            }
        });
        
        dropZone.addEventListener("dragover", function(e) {
            e.preventDefault();
            // Efecto pulsante en el borde
            dropZone.style.borderColor = "var(--color-primary)";
            dropZone.style.boxShadow = "0 0 40px rgba(96, 165, 250, 0.3)";
        });
        
        dropZone.addEventListener("drop", function(e) {
            e.preventDefault();
            dragCounter = 0;
            dropZone.classList.remove("drag-over");
            dropZone.style.borderColor = "";
            dropZone.style.boxShadow = "";
            
            // Procesar archivos
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFiles(files);
            }
        });
    }

    // ============================================
    // PROGRESO INDIVIDUAL POR ARCHIVO
    // ============================================

    function handleFiles(files) {
        const fileList = document.getElementById("file-list");
        if (!fileList) return;
        
        Array.from(files).forEach(function(file, index) {
            // Crear elemento de archivo
            const item = document.createElement("div");
            item.className = "file-item";
            item.dataset.index = index;
            
            item.innerHTML = `
                <div class="file-info">
                    <span class="file-icon">📄</span>
                    <span class="file-name">${file.name}</span>
                    <span class="file-size">${formatFileSize(file.size)}</span>
                </div>
                <div class="file-progress">
                    <div class="progress-bar" style="width: 0%;"></div>
                </div>
                <div class="file-status">
                    <span class="status-text">⏳ Pendiente</span>
                </div>
            `;
            
            fileList.appendChild(item);
            
            // Simular subida con progreso
            simulateUpload(item, file);
        });
    }

    function simulateUpload(item, file) {
        const progressBar = item.querySelector(".progress-bar");
        const statusText = item.querySelector(".status-text");
        let progress = 0;
        
        // Actualizar estado a "Subiendo"
        statusText.textContent = "⬆️ Subiendo...";
        statusText.style.color = "var(--color-primary)";
        
        const interval = setInterval(function() {
            // Simular progreso con velocidad variable
            const increment = Math.random() * 15 + 5;
            progress = Math.min(progress + increment, 100);
            progressBar.style.width = progress + "%";
            
            if (progress >= 100) {
                clearInterval(interval);
                // Completado
                statusText.textContent = "✅ Completado";
                statusText.style.color = "var(--color-success)";
                progressBar.style.background = "var(--color-success)";
                
                // Mostrar notificación
                showNotification(`${file.name} subido correctamente`, "success");
            }
        }, 200);
    }

    // ============================================
    // UTILIDADES
    // ============================================

    function formatFileSize(bytes) {
        if (bytes === 0) return "0 B";
        const k = 1024;
        const sizes = ["B", "KB", "MB", "GB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    }

    function showNotification(message, type) {
        // Usar sistema de notificaciones global si existe
        if (window.Notifications) {
            window.Notifications.show(message, type);
        } else {
            console.log(`[${type}] ${message}`);
        }
    }

})();
