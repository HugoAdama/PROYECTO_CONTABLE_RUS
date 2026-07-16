## Hallazgo S3-01 — Instancias duplicadas de SQLAlchemy

Los modelos de `src/models/` dependen actualmente de `from app import db`,
mientras que la aplicación viva inicializa `db` desde
`src/database/conexion.py`.

La nueva arquitectura define una tercera ubicación prevista:
`contable/extensions.py`.

### Riesgo

Mover los modelos y cambiar sus imports de forma aislada puede provocar que
los modelos y la aplicación usen instancias diferentes de SQLAlchemy.

### Decisión

La migración de modelos y repositories se realizará como una unidad técnica.
La instancia definitiva será `contable.extensions.db`.

Durante esta transición se actualizarán todos los consumidores relacionados
antes de ejecutar la suite de pruebas.