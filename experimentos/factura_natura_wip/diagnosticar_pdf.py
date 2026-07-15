# diagnosticar_pdf.py
# ===================
# Script para diagnosticar la extracción de PDFs

import pdfplumber
import re
from pathlib import Path

# Probar con una factura
factura_path = Path(__file__).resolve().parents[2] / 'data/facturas/2026_05/20260712_180534_20101796532-01-F033-00330623.pdf'
if factura_path.exists():
    print('📄 Leyendo factura:', factura_path.name)
    print('=' * 60)
    with pdfplumber.open(factura_path) as pdf:
        text = pdf.pages[0].extract_text()
        print('🔍 TEXTO COMPLETO:')
        print(text)
        print('=' * 60)
        print('🔍 BUSCANDO PATRONES:')
        
        # Buscar número de factura
        num_match = re.search(r'F033\s*[-–]\s*\d{8}', text)
        print(f'  Número (F033-XXX): {num_match.group(0) if num_match else "NO"}')
        
        # Buscar RUC
        ruc_match = re.search(r'R\.U\.C[:\s]*(\d{11})', text)
        print(f'  RUC Emisor: {ruc_match.group(1) if ruc_match else "NO"}')
        
        # Buscar RUC Cliente
        ruc_cli = re.search(r'(?:DNI/RUC|RUC)[:\s]*(\d{11})', text)
        print(f'  RUC Cliente: {ruc_cli.group(1) if ruc_cli else "NO"}')
        
        # Buscar total
        total_match = re.search(r'Total a Pagar[:\s]*S/?\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
        print(f'  Total: {total_match.group(1) if total_match else "NO"}')
        
        # Buscar "S/ 191.70" al final
        total_match2 = re.search(r'S/?\s*([\d,]+\.?\d*)\s*$', text)
        print(f'  Total (final): {total_match2.group(1) if total_match2 else "NO"}')
        
        # Buscar "IMPORTE TOTAL"
        total_match3 = re.search(r'IMPORTE TOTAL[:\s]*([A-Z\s]+)\s*S/?\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
        print(f'  IMPORTE TOTAL: {total_match3.group(2) if total_match3 else "NO"}')
else:
    print('❌ Archivo no encontrado')
