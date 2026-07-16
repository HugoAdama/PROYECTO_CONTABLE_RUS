# Sprint 03 — Migración de módulos

## Fecha

15 de julio de 2026

## Objetivo

Migrar las capas internas del proyecto hacia el paquete `contable/`
sin modificar su comportamiento.

## Cambios realizados

- Migración de models.
- Migración de repositories.
- Migración de extractors.
- Migración de calculators.
- Migración de utils.
- Migración de services.
- Actualización de imports.
- Creación de puentes temporales en paquetes legacy.
- Eliminación del seguimiento de archivos `__pycache__` y `.pyc`.
- Registro de dependencias para cada capa migrada.

## Verificación

- Suite unitaria completa en verde.
- Pruebas de integración de servicios en verde.
- Pruebas de exportación en verde.
- Pruebas de rutas en verde.
- Suite completa en verde.
- Aplicación legacy inicia correctamente.
- Nueva Application Factory crea una instancia correctamente.

## Fuera de alcance

- División de `routes.py`.
- Implementación de `DocumentoService`.
- Implementación del POST `/subir`.
- Eliminación definitiva de `app/` y `src/`.
