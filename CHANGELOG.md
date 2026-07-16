# Changelog

Todos los cambios importantes del proyecto serán documentados aquí.

---

# v4.0 - Foundation Architecture

Fecha

15/07/2026

## Agregado

- Nuevo paquete contable/
- Application Factory
- extensions.py
- config.py
- wsgi.py
- Documentación de arquitectura
- ADR-001
- GLOSARIO
- Arquitectura por capas

## Seguridad

- Eliminado SECRET_KEY hardcodeado
- Configuración preparada para producción

## Documentación

- CAPAS_DEL_SISTEMA
- ROADMAP
- DECISIONES_ARQUITECTURA

---

# Próxima versión

# v5.0 — Migración de Capas

## Agregado

- Nueva ubicación definitiva para modelos.
- Nueva ubicación definitiva para repositorios.
- Nueva ubicación definitiva para extractores.
- Nueva ubicación definitiva para calculadoras.
- Nueva ubicación definitiva para utilidades.
- Nueva ubicación definitiva para servicios.

## Cambiado

- Imports actualizados al paquete `contable`.
- SQLAlchemy compartido temporalmente entre arquitectura legacy y nueva.
- Servicios vivos migrados sin modificar comportamiento.

## Mantenimiento

- Eliminados archivos `.pyc` del control de versiones.
- Añadidas reglas de caché Python a `.gitignore`.

## Pruebas

- Suite completa en verde después de la migración.
## [4.4.0] - 2026-07-15

### Arquitectura
- Se dividió `app/routes.py` en módulos bajo `contable/api` conservando los endpoints `main.*`.
- Se añadió la ruta de exportación Excel y se conectó con la pantalla de reportes.

### Procesamiento de documentos
- Se implementó `DocumentoService` como orquestador de detección, extracción, normalización y persistencia.
- Se conectó `/api/upload` al nuevo flujo.
- Se incorporaron validaciones de tipo, número, fecha, monto y duplicados.
- Se corrigió la detección de comprobantes de percepción frente a facturas que contienen líneas de percepción.

### Pruebas
- 56 pruebas automatizadas aprobadas.
- Flujo validado con 7 PDFs reales: 3 facturas, 3 boletas y 1 percepción.

## [5.0.0] - 2026-07-16
### Added
- Interfaz Liquid Glass responsive, clara y oscura.
- Animaciones ambientales de luz y gotas con accesibilidad de movimiento reducido.
- Gráficos offline, carga múltiple con feedback y backups descargables.
### Changed
- Todas las páginas consumen datos reales y comparten un contexto global consistente.
- Dashboard usa el último período con información disponible.
