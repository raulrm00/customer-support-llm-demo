# Contexto del proyecto

El proyecto ya dispone de:

- Un backend existente desarrollado con FastAPI.
- Un frontend existente desarrollado con Angular + TailwindCSS.
- Toda la infraestructura funciona en un entorno Dockerizado.
- La aplicación ya expone una API REST que actualmente consume el frontend Angular.
- Se utiliza PostgreSQL como base de datos principal.
- El objetivo es añadir un sistema completo de autenticación, autorización básica y control de consumo diario de la API sin romper la arquitectura existente.

---

# Objetivo

Implementar un sistema de autenticación de usuarios completo para el proyecto existente.

La solución debe:

1. Integrarse sobre el backend FastAPI ya existente.
2. Integrarse con el frontend Angular ya existente.
3. Utilizar PostgreSQL como persistencia.
4. Funcionar correctamente dentro del entorno Docker ya existente.
5. Generar usuarios de prueba automáticamente.
6. Generar tests automáticos backend.
7. Proteger toda la API para que únicamente puedan consumirla usuarios autenticados.
8. Añadir un sistema de límites de consumo diario de tiempo de procesamiento de API por usuario.
9. Reiniciar automáticamente el consumo diario cada 24 horas.

---

# Requisitos técnicos backend (FastAPI)

## Autenticación

Implementar autenticación basada en JWT.

Requisitos:

- Login mediante email y contraseña.
- Registro de usuarios.
- Hash seguro de contraseñas usando passlib o bcrypt.
- Access Token JWT.
- Refresh Token JWT opcional pero recomendado.
- Middleware/dependency global de autenticación.
- Endpoints protegidos.
- Validación de expiración de tokens.
- Logout seguro en frontend.

---

# Modelo de usuario

Crear entidad User en PostgreSQL.

Campos mínimos:

```python
id
email
password_hash
is_active
is_admin
created_at
updated_at
daily_usage_seconds
daily_usage_reset_at
daily_limit_seconds
```

Recomendaciones:

- `daily_usage_seconds` almacena el tiempo consumido acumulado del día.
- `daily_usage_reset_at` almacena la última fecha de reinicio.
- `daily_limit_seconds` define el límite máximo diario permitido.

---

# Sistema de límites diarios

## Objetivo

Cada usuario tendrá un límite diario de uso de la API basado en tiempo de procesamiento consumido.

Ejemplo:

- Usuario con límite de 3600 segundos/día.
- Cada request suma el tiempo real de procesamiento.
- Cuando supere el límite:
  - devolver HTTP 429 Too Many Requests
  - devolver mensaje claro indicando límite diario excedido

---

# Funcionamiento esperado

## Medición de tiempo

Medir tiempo real de procesamiento por request:

```python
start_time = time.time()
...
processing_time = time.time() - start_time
```

Ese tiempo debe acumularse en:

```python
user.daily_usage_seconds
```

---

# Reinicio automático cada 24h

Antes de procesar cada request autenticada:

- Verificar si han pasado 24h desde `daily_usage_reset_at`
- Si han pasado:
  - reiniciar `daily_usage_seconds = 0`
  - actualizar `daily_usage_reset_at = now()`

No usar cron externo salvo que sea estrictamente necesario.

Preferible solución automática integrada en middleware/dependencies.

---

# Protección de API

Toda la API debe requerir autenticación excepto:

- login
- register
- healthcheck opcional

Todos los demás endpoints deben:

- validar JWT
- validar usuario activo
- validar límite diario

---

# Middleware / Dependency recomendada

Crear un middleware o dependency reusable que:

1. Valide JWT
2. Obtenga usuario
3. Reinicie límite diario si corresponde
4. Compruebe límite disponible
5. Ejecute request
6. Calcule tiempo consumido
7. Actualice consumo acumulado
8. Devuelva error 429 si supera límite

---

# Respuestas HTTP esperadas

## Usuario no autenticado

```json
{
  "detail": "Not authenticated"
}
```

HTTP:
```http
401 Unauthorized
```

---

## Token inválido

```json
{
  "detail": "Invalid token"
}
```

HTTP:
```http
401 Unauthorized
```

---

## Límite diario excedido

```json
{
  "detail": "Daily API usage limit exceeded"
}
```

HTTP:
```http
429 Too Many Requests
```

---

# Frontend Angular

## Objetivos frontend

Integrar sistema de autenticación completo en Angular.

Implementar:

- Login page
- Register page
- Auth service
- JWT interceptor
- Guards de rutas
- Logout
- Persistencia de sesión
- Manejo de expiración de token
- Pantalla/error de límite excedido

---

# Requisitos Angular

## Auth Service

Debe:

- guardar JWT
- recuperar JWT
- eliminar JWT
- comprobar autenticación
- exponer usuario actual

---

## HTTP Interceptor

Añadir automáticamente:

```http
Authorization: Bearer <token>
```

a todas las requests autenticadas.

---

## Route Guards

Proteger rutas privadas.

Si usuario no autenticado:

```typescript
this.router.navigate(['/login'])
```

---

# Docker

Actualizar docker-compose existente para incluir:

- PostgreSQL
- variables de entorno necesarias
- persistencia de datos
- networking correcto

---

# Variables de entorno

Definir:

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DATABASE_URL=

JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

DEFAULT_DAILY_LIMIT_SECONDS=3600
```

---

# Migraciones

Usar Alembic para migraciones.

Crear migraciones para:

- tabla users
- índices
- constraints

---

# Usuarios de prueba

Generar automáticamente usuarios de ejemplo al iniciar el proyecto si no existen.

Ejemplos:

```text
admin@example.com
user@example.com
```

Contraseña:

```text
password123
```

Admin:

- admin@example.com

Usuario normal:

- user@example.com

---

# Tests requeridos

Generar tests automáticos para:

## Auth

- login correcto
- login inválido
- acceso protegido
- JWT inválido
- JWT expirado

---

## Límites diarios

- consumo acumulado
- bloqueo por límite excedido
- reinicio automático tras 24h

---

## Integración

- flujo login frontend
- requests autenticadas
- interceptor JWT

---

# Librerías recomendadas backend

Preferiblemente usar:

```txt
fastapi
sqlalchemy
alembic
psycopg2-binary
python-jose
passlib[bcrypt]
pydantic
pytest
httpx
```

---

# Arquitectura recomendada

Separar:

```text
app/
├── api/
├── auth/
├── core/
├── db/
├── middleware/
├── models/
├── schemas/
├── services/
├── tests/
```

---

# Requisitos de calidad

El código generado debe:

- ser limpio y mantenible
- seguir buenas prácticas FastAPI
- usar tipado Python
- usar SQLAlchemy ORM
- ser modular
- incluir comentarios mínimos útiles
- evitar hardcodes
- usar variables de entorno
- incluir manejo de errores

---

# Resultado esperado

El resultado final debe permitir:

1. Registrar usuarios
2. Iniciar sesión
3. Consumir API autenticada
4. Bloquear usuarios al superar límite diario
5. Reiniciar límites automáticamente cada 24h
6. Ejecutarse completamente en Docker
7. Tener tests funcionales
8. Integrarse correctamente con Angular + Tailwind existentes
