/**
 * Sistema de paginación para tablas
 * Permite navegar por grandes conjuntos de datos
 */

class PaginadorTabla {
    constructor(tableId, options = {}) {
        this.table = document.getElementById(tableId);
        if (!this.table) return;
        
        this.tbody = this.table.querySelector('tbody');
        this.rows = Array.from(this.tbody?.querySelectorAll('tr') || []);
        this.options = {
            rowsPerPage: options.rowsPerPage || 10,
            maxButtons: options.maxButtons || 5,
            ...options
        };
        
        this.currentPage = 1;
        this.totalPages = Math.ceil(this.rows.length / this.options.rowsPerPage);
        
        this.render();
        this.createPaginationControls();
    }
    
    render() {
        const start = (this.currentPage - 1) * this.options.rowsPerPage;
        const end = start + this.options.rowsPerPage;
        
        // Ocultar todas las filas
        this.rows.forEach(row => row.style.display = 'none');
        
        // Mostrar solo las filas de la página actual
        this.rows.slice(start, end).forEach(row => row.style.display = '');
        
        // Actualizar información de paginación
        this.updateInfo();
    }
    
    createPaginationControls() {
        // Buscar o crear contenedor de paginación
        let container = this.table.parentElement.querySelector('.pagination-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'pagination-container glass-card';
            container.style.cssText = `
                padding: 12px 20px;
                margin-top: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            `;
            this.table.parentElement.appendChild(container);
        }
        
        // Información de registros
        const info = document.createElement('div');
        info.className = 'pagination-info';
        info.style.cssText = 'color: rgba(255,255,255,0.5); font-size: 0.85rem;';
        info.id = `pagination-info-${this.table.id}`;
        
        // Controles de navegación
        const controls = document.createElement('div');
        controls.className = 'pagination-controls';
        controls.style.cssText = 'display: flex; gap: 6px; align-items: center;';
        
        // Botón Anterior
        const prevBtn = this.createButton('‹', () => {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.render();
                this.updateControls();
            }
        });
        
        // Botones de página
        const pagesContainer = document.createElement('span');
        pagesContainer.id = `pagination-pages-${this.table.id}`;
        pagesContainer.style.cssText = 'display: flex; gap: 4px;';
        
        // Botón Siguiente
        const nextBtn = this.createButton('›', () => {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.render();
                this.updateControls();
            }
        });
        
        controls.appendChild(prevBtn);
        controls.appendChild(pagesContainer);
        controls.appendChild(nextBtn);
        
        // Selector de filas por página
        const selector = document.createElement('select');
        selector.className = 'glass-select';
        selector.style.cssText = 'padding: 4px 8px; font-size: 0.8rem; width: auto;';
        [10, 25, 50, 100].forEach(rows => {
            const option = document.createElement('option');
            option.value = rows;
            option.textContent = `${rows} filas`;
            if (rows === this.options.rowsPerPage) option.selected = true;
            selector.appendChild(option);
        });
        selector.addEventListener('change', (e) => {
            this.options.rowsPerPage = parseInt(e.target.value);
            this.totalPages = Math.ceil(this.rows.length / this.options.rowsPerPage);
            this.currentPage = 1;
            this.render();
            this.updateControls();
        });
        
        // Limpiar y agregar elementos
        container.innerHTML = '';
        container.appendChild(info);
        container.appendChild(controls);
        container.appendChild(selector);
        
        this.updateInfo();
        this.updateControls();
    }
    
    createButton(label, onClick) {
        const btn = document.createElement('button');
        btn.textContent = label;
        btn.className = 'btn-pagination';
        btn.style.cssText = `
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 8px;
            color: rgba(255,255,255,0.7);
            padding: 4px 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.85rem;
        `;
        btn.addEventListener('click', onClick);
        btn.addEventListener('mouseenter', () => {
            btn.style.background = 'rgba(255,255,255,0.08)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.background = 'rgba(255,255,255,0.04)';
        });
        return btn;
    }
    
    updateInfo() {
        const start = (this.currentPage - 1) * this.options.rowsPerPage + 1;
        const end = Math.min(start + this.options.rowsPerPage - 1, this.rows.length);
        const info = document.getElementById(`pagination-info-${this.table.id}`);
        if (info) {
            info.textContent = `Mostrando ${start}-${end} de ${this.rows.length} registros`;
        }
    }
    
    updateControls() {
        const pagesContainer = document.getElementById(`pagination-pages-${this.table.id}`);
        if (!pagesContainer) return;
        
        pagesContainer.innerHTML = '';
        
        // Calcular rango de páginas a mostrar
        let startPage = Math.max(1, this.currentPage - 2);
        let endPage = Math.min(this.totalPages, startPage + 4);
        if (endPage - startPage < 4) {
            startPage = Math.max(1, endPage - 4);
        }
        
        for (let i = startPage; i <= endPage; i++) {
            const btn = this.createButton(i.toString(), () => {
                this.currentPage = i;
                this.render();
                this.updateControls();
            });
            if (i === this.currentPage) {
                btn.style.background = 'rgba(102, 126, 234, 0.2)';
                btn.style.borderColor = 'rgba(102, 126, 234, 0.3)';
                btn.style.color = '#fff';
            }
            pagesContainer.appendChild(btn);
        }
    }
}

// Inicializar paginación en todas las tablas con clase 'table-paginada'
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('table.table-paginada').forEach(table => {
        new PaginadorTabla(table.id || 'tabla-default', {
            rowsPerPage: 10,
            maxButtons: 5
        });
    });
});