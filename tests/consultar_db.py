import sqlite3

conn = sqlite3.connect('contable.db')
cursor = conn.cursor()

# Ver todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

for tabla in tablas:
    nombre = tabla[0]
    print(f"\n📊 TABLA: {nombre}")
    print("-" * 40)
    
    # Ver estructura de la tabla
    cursor.execute(f"PRAGMA table_info({nombre})")
    columnas = cursor.fetchall()
    for col in columnas:
        print(f"  {col[1]} ({col[2]})")
    
    # Ver primeros 3 registros
    cursor.execute(f"SELECT * FROM {nombre} LIMIT 3")
    rows = cursor.fetchall()
    if rows:
        print(f"\n  Primeros registros:")
        for row in rows:
            print(f"    {row}")
    else:
        print(f"\n  ⚠️ Tabla vacía")

conn.close()