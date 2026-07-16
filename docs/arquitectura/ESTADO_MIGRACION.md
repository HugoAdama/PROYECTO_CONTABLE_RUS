# Estado de la Migración

## Sprint 1
✅ Completado

## Sprint 2
✅ Completado

## Sprint 3
✅ Models
✅ Repositories
✅ Extractors
✅ Calculators
✅ Utils
✅ Services

## Sprint 4
✅ `contable/api` creado
✅ `app/routes.py` dividido por responsabilidades
✅ Dashboard, documentos, reportes, exportación, configuración y carpetas separados
✅ Endpoints `main.*` conservados

## Sprint 5
✅ `DocumentoService` implementado como orquestador
✅ Detección automática del tipo de PDF
✅ Extracción especializada por tipo
✅ Normalización al modelo unificado `Documento`
✅ Control de duplicados
✅ Persistencia e historial integrados
✅ Endpoint `/api/upload` conectado al nuevo flujo

Verificaciones ejecutadas y documentadas en `docs/sprint-reports/sprint-04-05.md`.

Último commit base recibido:
`refactor(sprint-3): migrate domain modules to contable package`

## Próximo Sprint

Sprint 6

Objetivo:
Eliminar definitivamente el código legado cuando la validación funcional con datos reales confirme el nuevo flujo.
