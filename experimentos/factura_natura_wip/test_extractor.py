import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# test_extractor.py
# =================
# Script para probar el extractor con un PDF real

from pathlib import Path
import pdfplumber
from factura_natura import FacturaNaturaExtractor

# Probar con una factura
factura_path = Path(__file__).resolve().parents[2] / 'data/facturas/2026_05/20260712_180534_20101796532-01-F033-00330623.pdf'
if factura_path.exists():
    print('📄 Probando factura:', factura_path.name)
    print('=' * 50)
    with pdfplumber.open(factura_path) as pdf:
        text = pdf.pages[0].extract_text()
        extractor = FacturaNaturaExtractor()
        data = extractor.extract(text)
        print('📊 DATOS EXTRAÍDOS:')
        print(f'  Número: {data["numero"]}')
        print(f'  RUC Emisor: {data["ruc_emisor"]}')
        print(f'  RUC Cliente: {data["ruc_cliente"]}')
        print(f'  Nombre: {data["nombre_cliente"]}')
        print(f'  Fecha: {data["fecha_emision"]}')
        print(f'  Total: S/{data["monto_total"]:.2f}')
        print(f'  Percepción: S/{data["percepcion"]:.2f}')
        print(f'  Subtotal: S/{data["monto_base"]:.2f}')
        print(f'  Ciclo: {data["ciclo"]}')
        print('=' * 50)
        if data["numero"] and data["monto_total"] > 0:
            print('✅ EXTRACCIÓN EXITOSA')
        else:
            print('❌ EXTRACCIÓN FALLIDA')
else:
    print('❌ Archivo no encontrado')
