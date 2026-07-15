/**
 * MODULES: CHARTS
 * Sistema de Control Financiero RUS v3.9.1
 * 
 * Maneja los gráficos interactivos con Plotly
 */

class ChartsModule {
    constructor() {
        this.data = window.datosReportes || null;
        this.init();
    }
    
    init() {
        if (!this.data) {
            console.log('📊 No hay datos de reportes disponibles');
            return;
        }
        
        console.log('📊 Inicializando gráficos...');
        this.renderVentasChart();
        this.renderComprasChart();
        this.renderImpuestosChart();
        this.renderDistribucionChart();
    }
    
    renderVentasChart() {
        const container = document.getElementById('grafico-ventas');
        if (!container) return;
        
        const ventas = this.data.ventas_por_mes || {};
        const meses = Object.keys(ventas).sort();
        const valores = meses.map(m => ventas[m]);
        
        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#ffffff', size: 14 },
            margin: { l: 60, r: 20, t: 40, b: 50 },
            xaxis: { 
                gridcolor: 'rgba(255,255,255,0.05)',
                tickfont: { size: 12 }
            },
            yaxis: { 
                gridcolor: 'rgba(255,255,255,0.05)',
                tickfont: { size: 12 },
                tickprefix: 'S/ '
            },
            hovermode: 'x unified'
        };
        
        const trace = {
            x: meses,
            y: valores,
            type: 'bar',
            marker: {
                color: '#60a5fa',
                opacity: 0.8,
                line: { color: '#3b82f6', width: 1 }
            },
            hovertemplate: 'Ventas: S/ %{y:.2f}<extra></extra>'
        };
        
        Plotly.newPlot(container, [trace], layout, { responsive: true });
    }
    
    renderComprasChart() {
        const container = document.getElementById('grafico-compras');
        if (!container) return;
        
        const compras = this.data.compras_por_mes || {};
        const meses = Object.keys(compras).sort();
        const valores = meses.map(m => compras[m]);
        
        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#ffffff', size: 14 },
            margin: { l: 60, r: 20, t: 40, b: 50 },
            xaxis: { 
                gridcolor: 'rgba(255,255,255,0.05)',
                tickfont: { size: 12 }
            },
            yaxis: { 
                gridcolor: 'rgba(255,255,255,0.05)',
                tickfont: { size: 12 },
                tickprefix: 'S/ '
            },
            hovermode: 'x unified'
        };
        
        const trace = {
            x: meses,
            y: valores,
            type: 'bar',
            marker: {
                color: '#4ade80',
                opacity: 0.8,
                line: { color: '#22c55e', width: 1 }
            },
            hovertemplate: 'Compras: S/ %{y:.2f}<extra></extra>'
        };
        
        Plotly.newPlot(container, [trace], layout, { responsive: true });
    }
    
    renderImpuestosChart() {
        const container = document.getElementById('grafico-impuestos');
        if (!container) return;
        
        const impuestos = this.data.impuestos_por_mes || {};
        const meses = Object.keys(impuestos).sort();
        const valores = meses.map(m => impuestos[m]);
        
        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#ffffff', size: 14 },
            margin: { l: 60, r: 20, t: 40, b: 50 },
            xaxis: { 
                gridcolor: 'rgba(255,255,255,0.05)',
                tickfont: { size: 12 }
            },
            yaxis: { 
                gridcolor: 'rgba(255,255,255,0.05)',
                tickfont: { size: 12 },
                tickprefix: 'S/ '
            },
            hovermode: 'x unified'
        };
        
        const trace = {
            x: meses,
            y: valores,
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#fbbf24', width: 3 },
            marker: { color: '#fbbf24', size: 8 },
            fill: 'tozeroy',
            fillcolor: 'rgba(251,191,36,0.1)',
            hovertemplate: 'Impuestos: S/ %{y:.2f}<extra></extra>'
        };
        
        Plotly.newPlot(container, [trace], layout, { responsive: true });
    }
    
    renderDistribucionChart() {
        const container = document.getElementById('grafico-distribucion');
        if (!container) return;
        
        const distribucion = this.data.distribucion || {};
        const labels = Object.keys(distribucion);
        const values = Object.values(distribucion);
        
        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#ffffff', size: 14 },
            margin: { l: 20, r: 20, t: 40, b: 20 },
            showlegend: true,
            legend: { 
                orientation: 'v',
                x: 0.95,
                y: 0.95,
                font: { size: 12 }
            }
        };
        
        const colors = ['#60a5fa', '#4ade80', '#fbbf24', '#f87171', '#a78bfa'];
        
        const trace = {
            labels: labels,
            values: values,
            type: 'pie',
            marker: { colors: colors.slice(0, labels.length) },
            textinfo: 'label+percent',
            textposition: 'outside',
            hovertemplate: '%{label}: S/ %{value:.2f}<extra></extra>'
        };
        
        Plotly.newPlot(container, [trace], layout, { responsive: true });
    }
}

// ============================================
// INICIALIZAR
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new ChartsModule();
});