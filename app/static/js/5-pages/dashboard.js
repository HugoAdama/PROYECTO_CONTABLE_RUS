/**
 * Dashboard - Microinteracciones
 * Mejora la experiencia del usuario con feedback visual
 */

(function() {
    "use strict";

    // ============================================
    // ANIMACIÓN DE CONTEO (Números que cuentan)
    // ============================================

    function animateNumber(element, target, duration = 1000) {
        if (!element) return;
        
        const start = 0;
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = start + (target - start) * easeOutCubic(progress);
            
            // Formatear el número
            const formatted = new Intl.NumberFormat("es-PE", {
                style: "currency",
                currency: "PEN",
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(current);
            
            element.textContent = formatted;
            
            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = new Intl.NumberFormat("es-PE", {
                    style: "currency",
                    currency: "PEN",
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }).format(target);
            }
        }
        
        function easeOutCubic(t) {
            return 1 - Math.pow(1 - t, 3);
        }
        
        requestAnimationFrame(update);
    }

    // ============================================
    // HOVER EN TARJETAS (Efecto brillo)
    // ============================================

    document.querySelectorAll(".card-liquid").forEach(function(card) {
        card.addEventListener("mouseenter", function(e) {
            // Obtener posición del mouse relativa a la tarjeta
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            // Actualizar posición del brillo
            card.style.setProperty("--mouse-x", x + "%");
            card.style.setProperty("--mouse-y", y + "%");
        });
    });

    // ============================================
    // FEEDBACK DE CARGA EN BOTONES
    // ============================================

    document.querySelectorAll(".btn").forEach(function(button) {
        button.addEventListener("click", function(e) {
            if (button.dataset.loading) return;
            
            // Si el botón tiene atributo data-loading-text
            if (button.dataset.loadingText) {
                const originalText = button.innerHTML;
                button.dataset.originalText = originalText;
                button.dataset.loading = "true";
                button.innerHTML = `<span class="spinner"></span> ${button.dataset.loadingText}`;
                button.disabled = true;
                
                // Restaurar después de 2 segundos (simulación)
                setTimeout(function() {
                    button.innerHTML = button.dataset.originalText;
                    button.dataset.loading = "false";
                    button.disabled = false;
                }, 2000);
            }
        });
    });

    // ============================================
    // INICIALIZAR ANIMACIONES DE CONTEO
    // ============================================

    // Detectar elementos con clase "animate-number"
    document.querySelectorAll(".animate-number").forEach(function(element) {
        const target = parseFloat(element.dataset.target);
        if (!isNaN(target)) {
            // Usar Intersection Observer para animar solo cuando sea visible
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        animateNumber(element, target);
                        observer.unobserve(element);
                    }
                });
            }, { threshold: 0.5 });
            
            observer.observe(element);
        }
    });

})();
