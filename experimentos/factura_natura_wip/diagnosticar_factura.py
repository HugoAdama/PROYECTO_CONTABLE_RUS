# diagnosticar_factura.py
import pdfplumber
from pathlib import Path

factura_path = Path(__file__).resolve().parents[2] / 'data/facturas/2026_05/20260712_180533_20101796532-01-F033-00331167.pdf'
if factura_path.exists():
    with pdfplumber.open(factura_path) as pdf:
        text = pdf.pages[0].extract_text()
        print("=" * 60)
        print("TEXTO COMPLETO:")
        print("=" * 60)
        print(text)
        print("=" * 60)
        print("BUSCANDO FECHA:")
        import re
        fecha_match = re.search(r'Fecha Emisión[:\s]*(\d{1,2}/\d{1,2}/\d{4})', text)
        if fecha_match:
            print(f"✅ Fecha encontrada: {fecha_match.group(1)}")
        else:
            print("❌ No se encontró 'Fecha Emisión'")
            # Buscar cualquier fecha
            fechas = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', text)
            if fechas:
                print(f"  Otras fechas encontradas: {fechas}")
            else:
                print("  No se encontraron fechas en el texto")
else:
    print("Archivo no encontrado")
