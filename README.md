# Proyecto GPS 26-27 (GA05)

Aplicación web del festival **Subsonic Fest**: backend en FastAPI con MongoDB y frontend SPA en HTML/CSS/JS vanilla.

**Miembros del grupo:**
- Jaime Arias Rodríguez
- Manuel Carvajal Tarifa
- Justo Cilleros Rodríguez
- Javier García Espina
- Álvaro Martín Rodríguez

---

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (para MongoDB)
- Python 3.13+
- Git

## Cómo ejecutar la aplicación

### 1. Levantar MongoDB

Desde la raíz del proyecto:

```bash
docker compose up -d
```

Esto arranca el contenedor `subsonic-mongodb` en `localhost:27017` con un volumen persistente (`subsonic-mongo-data`).

### 2. Crear el entorno virtual e instalar dependencias

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Configurar variables de entorno (opcional)

La aplicación funciona con los valores por defecto pensados para local. Si quieres personalizarlos:

```bash
cp backend/.env.example backend/.env
```

### 4. Arrancar el backend

```bash
python backend/src/main.py
```

También puedes usar Uvicorn directamente:

```bash
cd backend/src
uvicorn controller.controller:app --reload --port 8000
```

### 5. Abrir la aplicación

Con el backend en marcha, abre:

- **Aplicación:** http://localhost:8000/
- **API / documentación:** http://localhost:8000/docs
- **Estado del servicio:** http://localhost:8000/api/health

El frontend se sirve desde el propio backend, así que no hace falta levantar otro servidor.

En el primer arranque se cargan automáticamente datos de demostración (usuarios, eventos, productos, artistas y pedidos). Se puede desactivar con `SEED_DEMO_DATA=False`.

## Credenciales de demostración

| Rol | Email | Contraseña |
|---|---|---|
| Cliente | `cliente.demo@subsonicfest.com` | `Cliente123!` |
| Proveedor | `proveedor.demo@subsonicfest.com` | `Proveedor123!` |
| Gestor | `gestor.demo@subsonicfest.com` | `Gestor123!` |
| Admin | `admin.demo@subsonicfest.com` | `Admin123!` |

## Tests

```bash
python -m pytest backend/tests -q
```

## Parar la aplicación

```bash
# Detener el backend: Ctrl+C en su terminal

# Detener MongoDB
docker compose down

# Detener MongoDB y borrar los datos
docker compose down -v
```

## Estructura del proyecto

```
backend/
  src/
    config/       Configuración y carga de .env
    controller/   App FastAPI y routers (core, auth, RBAC, perfil)
    model/        DAOs, DTOs, factorías e interfaces
    security/     JWT, hashing de contraseñas y RBAC
    services/     Lógica de negocio (usuarios, stock, reset de contraseña)
    scripts/      Seed de datos de demostración
  tests/          Tests con pytest
frontend/
  index.html      Shell de la SPA
  js/             Router, cliente de API y lógica por página
  paginas/        Plantillas HTML cargadas por el router
  css/            Estilos por página
docker-compose.yml
```
