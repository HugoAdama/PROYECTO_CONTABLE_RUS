/**
 * MODULE: CHARTS
 * Maneja los gráficos con Plotly
 */

const ChartsModule = (function() {
    'use strict';
    
    /**
     * Renderiza un gráfico de barras
     * @param {string} elementId - ID del elemento contenedor
     * @param {Object} data - Datos del gráfico
     * @param {Object} options - Opciones adicionales
     */
    function renderBarChart(elementId, data, options = {}) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const trace = {
            x: data.labels || [],
            y: data.values || [],
            type: 'bar',
            marker: {
                color: options.color || '#60a5fa',
                opacity: 0.85,
                line: { color: options.lineColor || '#3b82f6', width: 1 },
            },
            text: data.values ? data.values.map(v => FORMAT.currency(v)) : [],
            textposition: 'outside',
            hoverinfo: 'x+y',
        };
        
        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: 'rgba(255,255,255,0.6)', size: 12 },
            margin: { l: 70, r: 30, t: 40, b: 60 },
            yaxis: {
                title: options.yTitle || 'Monto (S/)',
                gridcolor: 'rgba(255,255,255,0.04)',
                tickformat: 'S/.2f',
                zeroline: true,
                zerolinecolor: 'rgba(255,255,255,0.04)',
            },
            xaxis: {
                title: options.xTitle || 'Mes',
                gridcolor: 'rgba(255,255,255,0.02)',
                tickangle: options.tickAngle || -30,
            },
            showlegend: false,
            hovermode: 'x unified',
            ...options.layout,
        };
        
        Plotly.newPlot(elementId, [trace], layout, { responsive: true });
    }
    
    /**
     * Renderiza un gráfico de líneas
     * @param {string} elementId - ID del elemento contenedor
     * @param {Object} data - Datos del gráfico
     * @param {Object} options - Opciones adicionales
     */
    function renderLineChart(elementId, data, options = {}) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const trace = {
            x: data.labels || [],
            y: data.values || [],
            type: 'scatter',
            mode: 'lines+markers',
            line: {
                color: options.color || '#fbbf24',
                width: 3,
                shape: 'spline',
            },
            marker: {
                color: options.markerColor || '#f59e0b',
                size: 10,
                symbol: 'circle',
                line: { color: '#fff', width: 1 },
            },
            fill: 'tozeroy',
            fillcolor: options.fillColor || 'rgba(251,191,36,0.1)',
            text: data.values ? data.values.map(v => FORMAT.currency(v)) : [],
            hoverinfo: 'x+y',
        };
        
        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: 'rgba(255,255,255,0.6)', size: 12 },
            margin: { l: 70, r: 30, t: 40, b: 60 },
            yaxis: {
                title: options.yTitle || 'Monto (S/)',
                gridcolor: 'rgba(255,255,255,0.04)',
                tickformat: 'S/.2f',
                zeroline: true,
                zerolinecolor: 'rgba(255,255,255,0.04)',
            },
            xaxis: {
                title: options.xTitle || 'Mes',
                gridcolor: 'rgba(255,255,255,0.02)',
                tickangle: options.tickAngle || -30,
            },
            showlegend: false,
            hovermode: 'x unified',
            ...options.layout,
        };
        
        Plotly.newPlot(elementId, [trace], layout, { responsive: true });
    }
    
    /**
     * Renderiza un gráfico de dona (pie)
     * @param {string} elementId - ID del elemento contenedor
     * @param {Object} data - Datos del gráfico
     * @param {Object} options - Opciones adicionales
     */
    function renderDoughnutChart(elementId, data, options = {}) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        if (!data.labels || data.labels.length === 0) {
            element.innerHTML = `
                <div style="display:flex;align-items:center;justify-content:center;height:100%;color:rgba(255,255,255,0.2);font-size:0.95rem;">
                    No hay datos disponibles
                </div>
            `;
            return;
        }
        
        const colors = options.colors || ['#4ade80', '#60a5fa', '#fbbf24', '#f87171', '#a78bfa', '#34d399', '#f472b6'];
        
        const trace = {
            values: data.values || [],
            labels: data.labels || [],
            type: 'pie',
            hole: 0.4,
            marker: {
                colors: colors.slice(0, data.labels.length),
            },
            textinfo: 'label+percent',
            textposition: 'auto',
            hoverinfo: 'label+value',
            hovertemplate: '%{label}<br>S/ %{value:,.2f}<br>%{percent}<extra></extra>',
            textfont: { color: 'rgba(255,255,255,0.7)', size: 11 },
        };
        
        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: 'rgba(255,255,255,0.5)', size: 12 },
            margin: { l: 20, r: 20, t: 20, b: 20 },
            showlegend: true,
            legend: {
                font: { color: 'rgba(255,255,255,0.4)', size: 11 },
                orientation: 'v',
                x: 1.05,
                y: 0.5,
            },
            ...options.layout,
        };
        
        Plotly.newPlot(elementId, [trace], layout, { responsive: true });
    }
    
    // API pública
    return {
        renderBarChart: renderBarChart,
        renderLineChart: renderLineChart,
        renderDoughnutChart: renderDoughnutChart,
    };
})();

// Exponer globalmente
if (typeof window !== 'undefined') {
    window.ChartsModule = ChartsModule;
}