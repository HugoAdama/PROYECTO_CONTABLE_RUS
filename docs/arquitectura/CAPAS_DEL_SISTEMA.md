# Arquitectura por Capas

## Objetivo

El proyecto Contable RUS utiliza una arquitectura por capas para separar responsabilidades y facilitar el mantenimiento, las pruebas y la escalabilidad.

Cada capa tiene una única responsabilidad y solamente puede comunicarse con determinadas capas.

---

# Flujo General

Usuario

↓

Frontend (HTML / CSS / JS)

↓

Blueprint (API)

↓

Service

↓

Repository

↓

Model

↓

Base de Datos

---

# Capa Frontend

Ubicación

contable/templates/

contable/static/

Responsabilidad

- Mostrar información al usuario.
- Validar datos simples.
- Realizar peticiones HTTP.

Nunca debe:

- Consultar la base de datos.
- Ejecutar reglas de negocio.

---

# Capa API (Blueprints)

Ubicación

contable/api/

Responsabilidad

- Recibir Requests.
- Validar parámetros.
- Llamar a Services.
- Devolver HTML o JSON.

Nunca debe:

- Consultar SQLAlchemy.
- Ejecutar lógica de negocio.
- Leer PDFs.

---

# Capa Services

Ubicación

contable/services/

Responsabilidad

Aquí vive toda la lógica del negocio.

Ejemplos:

- Procesar documentos.
- Calcular reportes.
- Validar reglas RUS.
- Organizar archivos.

Los Services coordinan el trabajo entre:

Extractores

↓

Repositories

↓

Calculators

Nunca deben renderizar HTML.

---

# Capa Repositories

Ubicación

contable/repositories/

Responsabilidad

Toda consulta a la base de datos.

Ejemplos:

- guardar()
- actualizar()
- eliminar()
- buscar_por_id()

Nunca deben:

- Leer PDFs.
- Conocer Flask.
- Conocer Templates.

---

# Capa Extractors

Ubicación

contable/extractors/

Responsabilidad

Extraer información de los documentos PDF.

Nunca deben guardar información en la base de datos.

Solo devuelven datos.

---

# Capa Calculators

Ubicación

contable/calculators/

Responsabilidad

Contener cálculos matemáticos.

Ejemplos

- impuestos
- utilidad
- proyecciones
- límites RUS

Nunca deben conocer SQLAlchemy.

---

# Capa Models

Ubicación

contable/models/

Responsabilidad

Representar tablas de la base de datos.

No contienen lógica del negocio.

---

# Regla de Oro

Ninguna capa puede saltarse otra.

Ejemplo correcto:

Blueprint

↓

Service

↓

Repository

↓

Model

↓

DB

Ejemplo incorrecto:

Blueprint

↓

Repository

↓

DB

---

# Dependencias Permitidas

Frontend

↓

API

↓

Services

↓

Repositories

↓

Models

↓

Database

Extractors

↓

Services

Calculators

↓

Services

Models

↓

Repositories

Nunca al revés.