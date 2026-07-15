# src/utils/cargar_estilos.py
"""
🎨 CARGA DE ESTILOS
Carga los estilos CSS desde un archivo externo
"""

import streamlit as st
from pathlib import Path

def cargar_estilos():
    """Carga el archivo de estilos CSS"""
    ruta_estilos = Path(__file__).parent.parent.parent / "dashboard" / "assets" / "estilos.css"
    
    try:
        with open(ruta_estilos, "r", encoding="utf-8") as f:
            estilos = f.read()
        st.markdown(f"<style>{estilos}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Si no existe el archivo, usar estilos básicos
        st.markdown("""
        <style>
            .stApp { background: #0f0c29; }
            .main-title { color: white; font-size: 2rem; text-align: center; }
        </style>
        """, unsafe_allow_html=True)