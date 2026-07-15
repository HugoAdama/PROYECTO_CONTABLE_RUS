import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# debug_extractor.py
import pdfplumber
from pathlib import Path
from factura_natura import FacturaNaturaExtractor

factura_path = Path(__file__).resolve().parents[2] / 'data/facturas/2026_05/20260712_180533_20101796532-01-F033-00331167.pdf'
if factura_path.exists():
    print("📄 Procesando:", factura_path.name)
    with pdfplumber.open(factura_path) as pdf:
        text = pdf.pages[0].extract_text()
        extractor = FacturaNaturaExtractor()
        data = extractor.extract(text)
        print("\n📊 DATOS EXTRAÍDOS:")
        for key, value in data.items():
            print(f"  {key}: {value}")
        print("\n" + "=" * 50)
        if data.get('fecha_emision'):
            print("✅ FECHA ENCONTRADA:", data['fecha_emision'])
        else:
            print("❌ FECHA VACÍA - Este es el problema!")
            print("📌 Buscando en el texto...")
            import re
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if 'Fecha' in line:
                    print(f"  Línea {i}: {line}")
else:
    print("Archivo no encontrado")
