PROYECTO CONTABLE RUS
Documento Maestro de Estado del Proyecto (Versión Base)

Fecha: 15 de julio de 2026

1. Objetivo del proyecto

Contable RUS es un sistema desarrollado en Python + Flask + SQLAlchemy + SQLite cuyo objetivo es ayudar a pequeños emprendedores acogidos al Régimen Único Simplificado (RUS) del Perú a registrar y controlar sus documentos de compras y ventas de forma sencilla, reduciendo al mínimo el trabajo manual.

El proyecto está orientado principalmente a usuarios con poca experiencia tecnológica. Por ello, la prioridad del sistema es la simplicidad de uso y la automatización del procesamiento de documentos.

2. Estado general del proyecto

Actualmente el proyecto es completamente funcional para determinadas operaciones, pero presenta una diferencia importante entre la arquitectura diseñada originalmente y la arquitectura que realmente utiliza la aplicación.

En términos generales, el proyecto puede dividirse en dos grandes partes:

Código vivo: utilizado por la aplicación en producción.
Código planificado: arquitectura más limpia que fue iniciada, pero nunca terminó de integrarse.

La refactorización propuesta tiene como objetivo unificar ambos mundos sin perder funcionalidad.

3. Flujo real de la aplicación (Estado actual)

Actualmente la aplicación procesa los documentos siguiendo este flujo:

Usuario

↓

routes.py

↓

ventas_service.py

↓

procesador_pdfs.py

↓

pdfplumber

↓

SQLAlchemy

↓

SQLite

Este es el flujo que realmente está en funcionamiento.

4. Arquitectura objetivo

El objetivo del proyecto es migrar progresivamente hacia una arquitectura en capas.

Usuario

↓

Blueprint Documentos

↓

DocumentoService

↓

DetectorExtractor

↓

Extractor especializado

↓

Repository

↓

Base de datos

Esta arquitectura ya existe parcialmente dentro del proyecto, pero todavía no está conectada.

5. Estado de cada módulo
app/

Actualmente contiene la aplicación Flask principal.

Sigue siendo el punto de entrada real del sistema.

No debe eliminarse hasta el Sprint 6.

src/

Contiene la mayor parte de la lógica utilizada por la aplicación.

Actualmente es el núcleo funcional del proyecto.

extractors/

Existen extractores especializados para:

Facturas
Boletas
Percepciones
Detector automático

Estos módulos funcionan y han sido probados anteriormente.

Actualmente no son utilizados por el flujo principal.

repositories/

Implementan el patrón Repository.

Funcionan correctamente.

No deben reescribirse.

Solo deberán conectarse nuevamente mediante DocumentoService.

DocumentoService

Actualmente es un servicio vacío.

Sus métodos contienen únicamente pass.

Debe convertirse en el orquestador principal durante el Sprint 5.

procesador_pdfs.py

Actualmente realiza toda la extracción directamente utilizando pdfplumber.

Es el componente que mantiene funcionando la aplicación hoy.

Será reemplazado gradualmente por DocumentoService.

6. Estado de los documentos soportados

Actualmente el sistema trabaja principalmente con tres tipos de comprobantes.

Facturas de compra

Ejemplos analizados:

F033-00330022
F033-00330623
F033-00331167

Todas presentan una estructura muy similar:

proveedor
RUC
fecha emisión
fecha vencimiento
importe total
percepción
detalle de productos
Comprobantes de percepción

Ejemplo:

P003-00602821

Se encuentran asociados a una factura previamente emitida.

Representan compras.

Boletas de venta

Ejemplos:

EB01-302
EB01-303
EB01-304

Representan ventas realizadas por la usuaria.

Incluyen:

cliente
productos
importe total
7. Modelo de negocio

El sistema fue diseñado para una emprendedora que vende productos de belleza.

Actualmente recibe principalmente comprobantes de:

Natura
Avon

Sin embargo, el sistema NO debe depender de estos proveedores.

Los proveedores son únicamente datos extraídos del documento.

La arquitectura debe permitir registrar cualquier proveedor futuro sin modificaciones al código.

8. Principios de diseño adoptados

Durante toda la refactorización se seguirán estos principios.

1. El sistema nunca dependerá de un proveedor específico.

Incorrecto:

if proveedor == "Natura":

Correcto:

Factura

↓

Extraer proveedor

↓

Guardar proveedor
2. Cada responsabilidad tendrá una sola clase.

Ejemplo:

DetectorExtractor

solo detecta.

FacturaExtractor

solo extrae.

Repository

solo guarda.

DocumentoService

solo orquesta.

3. No duplicar lógica.

La lógica existente en los extractores será reutilizada.

No será reescrita.

4. Toda modificación debe ser reversible.

Por ello el proyecto se desarrollará mediante sprints independientes.

Cada sprint tendrá su propio commit.

9. Estado de la seguridad

Se identificaron las siguientes vulnerabilidades.

Críticas
SECRET_KEY hardcodeada.
debug=True por defecto.
configuración duplicada de DEBUG.
Medias
ausencia de .env.example
validación insuficiente de archivos

Estas vulnerabilidades serán resueltas durante el Sprint 1.

10. Estado de la arquitectura

Actualmente existen dos arquitecturas mezcladas.

Arquitectura antigua:

routes

↓

ventas_service

↓

procesador_pdfs

Arquitectura nueva:

Blueprint

↓

DocumentoService

↓

Extractores

↓

Repositories

El objetivo de la refactorización es migrar completamente a la segunda.

11. Roadmap oficial
Sprint 1

Seguridad.

No modifica funcionalidad.

Sprint 2

Creación del nuevo paquete

contable/
Sprint 3

Migración de módulos.

No reescribir.

Solo mover.

Sprint 4

Separación de Blueprints.

Sprint 5

Reconstrucción del flujo completo de carga de documentos.

Es el sprint más importante del proyecto.

Sprint 6

Eliminación definitiva del código legado.

12. Objetivo final

Al finalizar el proyecto, el sistema deberá permitir que un usuario:

Suba un PDF.
El sistema detecte automáticamente el tipo de documento.
Extraiga toda la información relevante.
Guarde los datos en la base de datos.
Actualice el dashboard automáticamente.
Genere reportes sin intervención manual.

Todo ello mediante una arquitectura limpia, modular y fácilmente mantenible.

13. Reglas de desarrollo

Estas reglas serán obligatorias durante toda la refactorización:

Ningún sprint modificará responsabilidades fuera de su alcance.
No se reescribirán módulos que ya funcionan sin una justificación técnica.
Cada cambio deberá ser verificable mediante pruebas o validaciones manuales.
Cada sprint finalizará con un commit independiente.
Antes de iniciar un sprint se presentará su backlog y se esperará aprobación.
Las decisiones arquitectónicas se documentarán para evitar que futuros desarrolladores vuelvan a discutir problemas ya resueltos.
14. Recomendaciones técnicas adicionales

Además del roadmap original, recomiendo incorporar las siguientes prácticas para que el proyecto sea sostenible a largo plazo:

Definir un estándar de código (Black + isort + Ruff) para mantener un estilo uniforme.
Añadir tipado estático progresivamente con typing, comenzando por los servicios y repositorios.
Centralizar el manejo de errores mediante excepciones propias (DocumentoError, ExtractorError, RepositoryError) en lugar de propagar excepciones genéricas.
Implementar un sistema de logging estructurado, registrando cada procesamiento de documento con identificador, tipo detectado, resultado y errores.
Incorporar migraciones de base de datos con Flask-Migrate/Alembic cuando la arquitectura contable/ esté consolidada, evitando depender únicamente de db.create_all().
Separar claramente la configuración por entornos (desarrollo, pruebas y producción) utilizando config.py y variables de entorno.
Documentar el flujo de procesamiento con un diagrama de arquitectura actualizado al finalizar el Sprint 5.
Mantener una cobertura de pruebas creciente, especialmente sobre DocumentoService, ya que será el núcleo de la nueva arquitectura.
Crear una carpeta docs/ donde se almacenen este documento, los ADR (Architecture Decision Records) y los reportes de cada sprint.
Evitar reglas específicas para proveedores (como Natura o Avon) dentro del núcleo del sistema; cualquier tratamiento especial deberá implementarse mediante extractores especializados o adaptadores, preservando un núcleo agnóstico.
Conclusión

Después del análisis del repositorio, del historial de cambios, del estado documentado y de los ejemplos reales de comprobantes, considero que el proyecto no necesita reescribirse, sino completar una migración arquitectónica que ya fue bien planteada pero quedó inconclusa.

La estrategia por sprints que definimos es adecuada porque minimiza riesgos, facilita la revisión de cambios y mantiene el sistema operativo durante toda la transición. Si se sigue el roadmap acordado, el resultado será una aplicación con una arquitectura moderna, mantenible y preparada para crecer, sin perder el conocimiento ni la lógica de negocio ya implementados.