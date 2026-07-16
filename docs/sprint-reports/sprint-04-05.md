# Reporte de Sprints 4 y 5 — Contable RUS 4.4.0

## Base de trabajo

Commit recibido: `0c60b33 refactor(sprint-3): migrate domain modules to contable package`.

## Sprint 4 — Separación de Blueprints

Se creó `contable/api` y se dividieron las rutas por responsabilidad:

- `dashboard.py`: dashboard, historial y backup.
- `documentos.py`: subida, consulta y API de documentos.
- `reportes.py`: vista de reportes.
- `exportar.py`: descarga Excel.
- `configuracion.py`: vista y API de configuración.
- `carpetas.py`: vista de carpetas.

`app/routes.py` queda como adaptador temporal para imports legacy. Se conservó el Blueprint `main` y los nombres de endpoint existentes.

## Sprint 5 — Flujo completo de carga

`DocumentoService` quedó implementado como orquestador del flujo:

1. Recibe la ruta segura del PDF guardado por la API.
2. Detecta automáticamente factura, boleta o percepción.
3. Ejecuta el extractor especializado.
4. Normaliza la salida al modelo unificado `Documento`.
5. Valida número, fecha y monto.
6. Rechaza duplicados por número de documento.
7. Persiste el documento y registra la acción en `Historial`.
8. Devuelve el contrato JSON esperado por la interfaz.

Se corrigió la detección de percepciones para evitar clasificar como percepción una factura que solo contiene una línea de percepción.

## Verificaciones

- `python -m compileall -q app contable`: aprobado.
- `pytest`: 56 pruebas aprobadas.
- Prueba funcional en base SQLite temporal con 7 PDFs reales: 7 procesados.
  - Facturas: 3.
  - Boletas: 3.
  - Percepciones: 1.
  - Historial: 7 registros.
- Verificación de endpoints y arranque de la fábrica Flask: aprobada.
- `git diff --check` sobre archivos de Sprints 4 y 5: aprobado.

## Riesgos pendientes

- El Sprint 6 todavía debe retirar código legacy (`src/processors`, adaptador `app/routes.py` y servicios duplicados) solo después de una validación funcional de usuario.
- La configuración de pruebas del factory legacy crea la base antes de aplicar overrides; conviene corregirlo antes de ampliar pruebas aisladas.
- El proyecto usa `db.create_all()` y aún no dispone de migraciones Alembic operativas.
- Se requiere una prueba guiada en la computadora final de Doña María para validar permisos, rutas, impresora/Excel y facilidad de uso.
