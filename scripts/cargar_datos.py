# cargar_datos.py
# ===============
# Script para cargar datos reales desde PDFs

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from src.database.conexion import db
from src.database.models import Documento
from src.processors.procesador_pdfs import ProcesadorPDFs
from datetime import datetime

def cargar_datos():
    """Carga datos reales desde los PDFs en data/"""
    print("🚀 Cargando datos reales de Doña María...")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        # Verificar si ya hay datos
        total = Documento.query.count()
        if total > 0:
            print(f"⚠️  Ya hay {total} documentos en la base de datos.")
            respuesta = input("¿Deseas eliminar los datos existentes y recargar? (s/N): ")
            if respuesta.lower() != 's':
                print("❌ Operación cancelada.")
                return
            
            # Eliminar datos existentes
            db.session.query(Documento).delete()
            db.session.commit()
            print("✅ Datos existentes eliminados.")
        
        # Buscar todos los PDFs en data/ (ruta absoluta, ya no depende de la carpeta actual)
        data_dir = Path(__file__).resolve().parent.parent / "data"
        pdf_files = list(data_dir.glob("**/*.pdf"))
        print(f"📄 Encontrados {len(pdf_files)} archivos PDF")
        
        procesados = 0
        errores = 0
        documentos = []
        
        for file_path in pdf_files:
            try:
                print(f"  📄 Procesando: {file_path.name}")
                
                # Procesar el PDF
                data = ProcesadorPDFs.procesar(file_path)
                
                # Verificar si ya existe
                existing = Documento.query.filter_by(numero=data['numero']).first()
                if existing:
                    print(f"    ⚠️  Ya existe: {data['numero']}")
                    continue
                
                # Asegurar que la fecha existe
                fecha_emision = data.get('fecha_emision')
                if not fecha_emision:
                    fecha_emision = datetime.now().strftime('%d/%m/%Y')
                    print(f"    ⚠️  Usando fecha actual: {fecha_emision}")
                
                # Crear el documento
                documento = Documento(
                    numero=data['numero'],
                    tipo=data['tipo'],
                    ruc_emisor=data.get('ruc_emisor', ''),
                    ruc_cliente=data.get('ruc_cliente', ''),
                    nombre_cliente=data.get('nombre_cliente', ''),
                    fecha_emision=datetime.strptime(fecha_emision, '%d/%m/%Y').date(),
                    monto_total=data['monto_total'],
                    monto_base=data.get('monto_base', 0),
                    percepcion=data.get('percepcion', 0),
                    archivo_original=data['archivo'],
                    documento_asociado=data.get('documento_asociado', ''),
                    ciclo=data.get('ciclo', '')
                )
                
                db.session.add(documento)
                db.session.commit()  # Commit inmediato después de cada documento
                
                procesados += 1
                documentos.append(data)
                print(f"    ✅ Procesado: {data['numero']} | S/{data['monto_total']:.2f}")
                
            except Exception as e:
                errores += 1
                print(f"    ❌ Error: {str(e)[:100]}")
                # IMPORTANTE: Rollback para limpiar la sesión después de un error
                db.session.rollback()
                continue
        
        print("\n" + "=" * 50)
        print("📊 RESULTADO DE LA CARGA:")
        print(f"  ✅ Procesados: {procesados}")
        print(f"  ❌ Errores: {errores}")
        print(f"  📄 Total: {procesados + errores}")
        
        if documentos:
            print("\n📄 Documentos cargados:")
            for doc in documentos:
                print(f"  - {doc['tipo']}: {doc['numero']} | S/{doc['monto_total']:.2f}")
        
        print("\n✅ Carga completada.")

if __name__ == '__main__':
    cargar_datos()
