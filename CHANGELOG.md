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