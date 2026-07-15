# init_fast.py
# ============
# Inicialización rápida de la base de datos

import sys
from pathlib import Path

# Agregar directorio raíz al path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

print("🗄️ Inicializando base de datos...")

try:
    from app import create_app
    from src.database.conexion import db
    
    # Crear aplicación (esto ya crea la base de datos)
    app = create_app()
    
    # Verificar que la base de datos existe
    db_path = ROOT_DIR / "data/rus.db"
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"✅ Base de datos creada correctamente")
        print(f"📁 Ubicación: {db_path.absolute()}")
        print(f"📊 Tamaño: {size} bytes")
    else:
        print("❌ La base de datos no se creó")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
