# 📍 Estado actual del proyecto (15 julio 2026)

Este documento explica **qué archivos usa realmente la app hoy** y qué quedó
suelto de intentos anteriores, para no perderse entre versiones.

## ✅ Lo que SÍ está conectado y corriendo

```
app/routes.py
   └─> src/services/ventas_service.py   (⚠️ ver aviso abajo)
         └─> src/processors/procesador_pdfs.py   (lee los PDFs directo con pdfplumber)
         └─> src/database/models.py, src/database/conexion.py
```

Las plantillas (`app/templates/*.html`) y los estilos Liquid Glass
(`app/static/css/*`, `app/static/js/*`) siguen igual, no se tocaron.

## ⚠️ Aviso crítico (ya corregido en esta limpieza)

`src/services/ventas_service.py` — el archivo del que depende **toda** la
app — no estaba subido a git (aparecía como "untracked"). Ya se agregó al
commit. Antes de este cambio, si se perdía la carpeta local, se perdía la
lógica completa de ventas/dashboard.

## 🗄️ Código que quedó desconectado (no se borró, solo se archivó)

- **`app/services/`** (`documento_service.py`, `export_service.py`,
  `reporte_service.py`, `notificacion_service.py`): ya no los usa
  `routes.py`. Siguen ahí porque los 54 tests de `tests/integration/`
  los prueban, pero **no representan lo que la app hace hoy**. El botón
  "Exportar a Excel" en Reportes tampoco está conectado a ningún endpoint
  todavía.
- **`src/extractors/`** (los 6 archivos que quedan: `base_extractor.py`,
  `boleta_extractor.py`, `factura_extractor.py`, `percepcion_extractor.py`,
  `detector_extractor.py`, `proveedores.py`): tampoco los usa la app —
  `procesador_pdfs.py` hace la extracción directo, sin pasar por estas
  clases. Solo los usa `documento_service.py` (que a su vez ya no lo usa
  nadie más que sus propios tests).

## 🧪 Experimento en curso: `experimentos/factura_natura_wip/`

Aquí se movieron (sin borrar nada) los archivos que eran una segunda versión
de los extractores, creados hoy mismo, junto con los scripts de depuración
que los usaban (`test_extractor.py`, `debug_extractor.py`,
`diagnosticar_factura.py`, `diagnosticar_pdf.py`). Antes vivían sueltos en
la raíz del proyecto y con nombres casi iguales a los de `src/extractors/`
(`base.py` vs `base_extractor.py`, etc.), lo que generaba confusión sobre
cuál era la versión "real".

Por el contenido de `debug_extractor.py`, parece que el objetivo era
arreglar la extracción de **fecha de emisión** en facturas de un proveedor
específico ("Natura") que el extractor genérico no leía bien. Quedó a medio
resolver (`❌ FECHA VACÍA - Este es el problema!`). Las rutas internas se
actualizaron para que los scripts sigan funcionando desde su nueva
ubicación; la lógica no se tocó.

## 🛠️ Scripts de mantenimiento: `scripts/`

Se movieron aquí `cargar_datos.py`, `init_fast.py` y `verificar_datos.py`
(antes en la raíz). Son utilidades para inicializar la base de datos y
cargar/verificar documentos reales — sí usan el código vivo de la app.
Ejecutarlos desde la raíz del proyecto, por ejemplo:

```
python scripts/verificar_datos.py
```

## 📌 Pendientes para decidir (no se tocaron, son decisión de Hugo)

1. Confirmar si `app/services/` (reportes, exportación, notificaciones) se
   va a reconectar pronto, o si se debe eliminar junto con sus tests para
   que la suite refleje la app real.
2. Decidir si el experimento de `factura_natura` se retoma o se descarta.
3. Conectar el botón "Exportar a Excel" a un endpoint real, o quitarlo
   mientras tanto.
