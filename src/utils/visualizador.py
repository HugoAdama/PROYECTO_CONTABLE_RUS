# src/utils/visualizador.py
"""
📊 VISUALIZADOR DE GRÁFICOS
Funciones para crear gráficos profesionales con Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import calendar

class VisualizadorGraficos:
    """
    Clase para generar gráficos profesionales para el dashboard.
    Todos los gráficos usan el tema oscuro con efectos Liquid Glass.
    """
    
    # Paleta de colores personalizada
    COLORES = {
        'primario': '#667eea',      # Morado claro
        'secundario': '#764ba2',    # Morado oscuro
        'exito': '#00b894',          # Verde
        'peligro': '#ff6b6b',        # Rojo
        'advertencia': '#fdcb6e',    # Amarillo
        'info': '#74b9ff',           # Azul claro
        'gradiente': ['#667eea', '#764ba2', '#f093fb', '#4facfe']
    }
    
    @staticmethod
    def tema_oscuro():
        """Configuración del tema oscuro para todos los gráficos"""
        return {
            'template': 'plotly_dark',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': '#ffffff', 'family': 'Arial'},
            'legend': {'font': {'color': '#ffffff'}}
        }
    
    @staticmethod
    def grafico_evolucion_ventas(datos_mensuales, titulo="📈 Evolución de Ventas"):
        """
        Gráfico de línea con la evolución de ventas mes a mes.
        
        Args:
            datos_mensuales (dict): { 'mes': 'Enero', 'ventas': 1500, 'compras': 800 }
            titulo (str): Título del gráfico
        
        Returns:
            plotly.graph_objects.Figure
        """
        if not datos_mensuales:
            return None
        
        df = pd.DataFrame(datos_mensuales)
        
        fig = go.Figure()
        
        # Línea de ventas
        fig.add_trace(go.Scatter(
            x=df['mes'],
            y=df['ventas'],
            name='Ventas',
            line=dict(color=VisualizadorGraficos.COLORES['exito'], width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 184, 148, 0.2)',
            mode='lines+markers',
            marker=dict(size=10, color=VisualizadorGraficos.COLORES['exito'])
        ))
        
        # Línea de compras
        if 'compras' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['mes'],
                y=df['compras'],
                name='Compras',
                line=dict(color=VisualizadorGraficos.COLORES['peligro'], width=3),
                fill='tozeroy',
                fillcolor='rgba(255, 107, 107, 0.2)',
                mode='lines+markers',
                marker=dict(size=10, color=VisualizadorGraficos.COLORES['peligro'])
            ))
        
        # Configuración
        fig.update_layout(
            title=dict(text=titulo, font=dict(size=24, color='white')),
            xaxis=dict(title='Mes', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Monto (S/)', gridcolor='rgba(255,255,255,0.1)'),
            hovermode='x unified',
            **VisualizadorGraficos.tema_oscuro()
        )
        
        # Anotaciones con valores
        for i, row in df.iterrows():
            fig.add_annotation(
                x=row['mes'],
                y=row['ventas'],
                text=f"S/ {row['ventas']:,.0f}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30,
                font=dict(color='white', size=10)
            )
        
        return fig
    
    @staticmethod
    def grafico_distribucion_clientes(datos_clientes, titulo="🥧 Distribución por Cliente"):
        """
        Gráfico de pastel con distribución de ventas por cliente.
        
        Args:
            datos_clientes (list): [{'cliente': 'Ana', 'monto': 500}, ...]
            titulo (str): Título del gráfico
        
        Returns:
            plotly.graph_objects.Figure
        """
        if not datos_clientes:
            return None
        
        df = pd.DataFrame(datos_clientes)
        
        # Top 5 clientes, el resto como "Otros"
        if len(df) > 5:
            top = df.nlargest(5, 'monto')
            otros = pd.DataFrame({
                'cliente': ['Otros'],
                'monto': [df[~df.index.isin(top.index)]['monto'].sum()]
            })
            df = pd.concat([top, otros], ignore_index=True)
        
        fig = go.Figure(data=[go.Pie(
            labels=df['cliente'],
            values=df['monto'],
            hole=0.4,
            marker=dict(colors=VisualizadorGraficos.COLORES['gradiente']),
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>S/ %{value:,.2f}<br>%{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(text=titulo, font=dict(size=24, color='white')),
            **VisualizadorGraficos.tema_oscuro()
        )
        
        return fig
    
    @staticmethod
    def grafico_comparativo(ventas, compras, mes, año, titulo="📊 Resumen del Mes"):
        """
        Gráfico de barras comparando ventas y compras.
        
        Args:
            ventas (float): Total de ventas
            compras (float): Total de compras
            mes (int): Mes
            año (int): Año
            titulo (str): Título del gráfico
        
        Returns:
            plotly.graph_objects.Figure
        """
        nombre_mes = calendar.month_name[mes]
        
        fig = go.Figure(data=[
            go.Bar(
                x=['Ventas', 'Compras'],
                y=[ventas, compras],
                name='Monto',
                marker=dict(
                    color=[VisualizadorGraficos.COLORES['exito'], 
                           VisualizadorGraficos.COLORES['peligro']],
                    line=dict(color='rgba(255,255,255,0.2)', width=1)
                ),
                text=[f"S/ {ventas:,.2f}", f"S/ {compras:,.2f}"],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>S/ %{y:,.2f}<extra></extra>'
            )
        ])
        
        # Agregar línea de utilidad
        utilidad = ventas - compras
        if utilidad > 0:
            fig.add_annotation(
                x=0.5,
                y=max(ventas, compras) * 0.9,
                text=f"💰 Utilidad: S/ {utilidad:,.2f}",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='#00b894',
                font=dict(color='#00b894', size=14)
            )
        
        fig.update_layout(
            title=dict(
                text=f"{titulo} - {nombre_mes} {año}",
                font=dict(size=24, color='white')
            ),
            xaxis=dict(title='Categoría', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Monto (S/)', gridcolor='rgba(255,255,255,0.1)'),
            showlegend=False,
            **VisualizadorGraficos.tema_oscuro()
        )
        
        return fig
    
    @staticmethod
    def grafico_heatmap_actividad(datos_diarios, mes, año, titulo="🔥 Actividad Diaria"):
        """
        Heatmap de actividad por día del mes.
        
        Args:
            datos_diarios (dict): {1: 150, 2: 300, ...} día: monto
            mes (int): Mes
            año (int): Año
            titulo (str): Título del gráfico
        
        Returns:
            plotly.graph_objects.Figure
        """
        if not datos_diarios:
            return None
        
        # Crear matriz para el heatmap
        dias_mes = calendar.monthrange(año, mes)[1]
        matriz = []
        
        for dia in range(1, dias_mes + 1):
            monto = datos_diarios.get(dia, 0)
            matriz.append(monto)
        
        # Crear figura con go.Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=[matriz],
            x=list(range(1, dias_mes + 1)),
            y=[f"{calendar.month_name[mes]} {año}"],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title="Monto (S/)",
                titleside="right",
                tickformat="S/ ,.0f"
            ),
            hovertemplate='Día %{x}<br>Monto: S/ %{z:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=titulo, font=dict(size=24, color='white')),
            xaxis=dict(title='Día del Mes', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Mes', gridcolor='rgba(255,255,255,0.1)'),
            height=250,
            **VisualizadorGraficos.tema_oscuro()
        )
        
        return fig
    
    @staticmethod
    def grafico_indicadores(ventas, compras, utilidad, impuesto, percepciones):
        """
        Gráfico de indicadores tipo gauge.
        
        Returns:
            plotly.graph_objects.Figure
        """
        fig = make_subplots(
            rows=1, cols=4,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, 
                   {'type': 'indicator'}, {'type': 'indicator'}]]
        )
        
        # Ventas
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=ventas,
            title={'text': "💰 Ventas"},
            domain={'row': 0, 'column': 0},
            gauge={'axis': {'range': [0, max(ventas * 1.2, 1000)]},
                   'bar': {'color': VisualizadorGraficos.COLORES['exito']}}
        ))
        
        # Compras
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=compras,
            title={'text': "📦 Compras"},
            domain={'row': 0, 'column': 1},
            gauge={'axis': {'range': [0, max(compras * 1.2, 1000)]},
                   'bar': {'color': VisualizadorGraficos.COLORES['peligro']}}
        ))
        
        # Utilidad
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=utilidad,
            title={'text': "💵 Utilidad"},
            domain={'row': 0, 'column': 2},
            gauge={'axis': {'range': [0, max(utilidad * 1.2, 1000)]},
                   'bar': {'color': VisualizadorGraficos.COLORES['info']}}
        ))
        
        # Impuesto
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=impuesto,
            title={'text': "💸 Impuesto"},
            domain={'row': 0, 'column': 3},
            gauge={'axis': {'range': [0, max(impuesto * 1.2, 100)]},
                   'bar': {'color': VisualizadorGraficos.COLORES['advertencia']}}
        ))
        
        fig.update_layout(
            height=250,
            grid={'rows': 1, 'columns': 4},
            **VisualizadorGraficos.tema_oscuro()
        )
        
        return fig
    
    @staticmethod
    def grafico_proyeccion(datos_historicos, mes_actual, año_actual):
        """
        Gráfico de proyección de impuestos basado en tendencia.
        
        Args:
            datos_historicos (list): [{'mes': 'Enero', 'ventas': 1500}, ...]
            mes_actual (int): Mes actual
            año_actual (int): Año actual
        
        Returns:
            plotly.graph_objects.Figure
        """
        if not datos_historicos or len(datos_historicos) < 3:
            return None
        
        df = pd.DataFrame(datos_historicos)
        
        # Calcular tendencia
        df['indice'] = range(len(df))
        z = np.polyfit(df['indice'], df['ventas'], 1)
        tendencia = np.polyval(z, df['indice'])
        
        # Proyección a 3 meses
        meses_futuros = [f"Proy {i+1}" for i in range(3)]
        ultimo_indice = len(df) - 1
        proyeccion = []
        
        for i in range(1, 4):
            valor = np.polyval(z, ultimo_indice + i)
            proyeccion.append(max(0, valor))
        
        # Crear figura
        fig = go.Figure()
        
        # Datos históricos
        fig.add_trace(go.Scatter(
            x=df['mes'],
            y=df['ventas'],
            name='Histórico',
            line=dict(color=VisualizadorGraficos.COLORES['primario'], width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ))
        
        # Línea de tendencia
        fig.add_trace(go.Scatter(
            x=df['mes'],
            y=tendencia,
            name='Tendencia',
            line=dict(color='rgba(255,255,255,0.3)', width=2, dash='dash'),
            mode='lines'
        ))
        
        # Proyección
        meses_completos = list(df['mes']) + meses_futuros
        valores_completos = list(df['ventas']) + proyeccion
        
        fig.add_trace(go.Scatter(
            x=meses_completos,
            y=valores_completos,
            name='Proyección',
            line=dict(color=VisualizadorGraficos.COLORES['advertencia'], width=2, dash='dot'),
            mode='lines+markers',
            marker=dict(size=6, symbol='diamond')
        ))
        
        # Área de confianza
        fig.add_trace(go.Scatter(
            x=meses_completos,
            y=[v * 1.1 for v in valores_completos],
            fill='tonexty',
            fillcolor='rgba(253, 203, 110, 0.1)',
            line=dict(color='rgba(253, 203, 110, 0)'),
            name='Rango estimado',
            showlegend=False
        ))
        
        fig.update_layout(
            title=dict(
                text="📈 Proyección de Ventas",
                font=dict(size=24, color='white')
            ),
            xaxis=dict(title='Mes', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Ventas (S/)', gridcolor='rgba(255,255,255,0.1)'),
            hovermode='x unified',
            **VisualizadorGraficos.tema_oscuro()
        )
        
        return fig

# Importar numpy para la proyección
import numpy as np