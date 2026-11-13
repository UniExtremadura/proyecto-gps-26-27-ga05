"""Aplicación FastAPI del proyecto Subsonic Fest.

Este módulo construye la app, registra los routers de la API y sirve el
frontend estático desde ``frontend/``. La persistencia se realiza contra el
contenedor local de MongoDB definido en ``docker-compose.yml``.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config.config import (
    ALLOWED_ORIGINS,
    DEBUG,
    EXTRA_ALLOWED_ORIGINS,
    FRONTEND_DIR,
    SEED_DEMO_DATA,
)

logger = logging.getLogger("subsonic")

API_DESCRIPTION = (
    "API del proyecto Subsonic Fest. Expone autenticación local, catálogo de "
    "eventos, productos, artistas, pedidos y paneles de gestión."
)


def _seed_database() -> None:
    """Siembra roles y datos de demostración si la base está disponible."""
    if not SEED_DEMO_DATA:
        return
    try:
        from scripts.seed_demo import seed_if_empty

        created = seed_if_empty()
        if created:
            logger.info("Datos de demostración disponibles: %s", created)
    except Exception as exc:  # pragma: no cover - el arranque no debe romperse
        logger.warning("No se pudieron sembrar datos de demostración: %s", exc)


@asynccontextmanager
async def lifespan(_: FastAPI):
    _seed_database()
    yield


app = FastAPI(
    title="Subsonic Fest API",
    description=API_DESCRIPTION,
    version="1.0.0",
    debug=DEBUG,
    lifespan=lifespan,
)

# CORS para el frontend local (VSCode Live Server, servidor estático, etc.).
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(dict.fromkeys(ALLOWED_ORIGINS + EXTRA_ALLOWED_ORIGINS)),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de la API (auth, catálogo, perfiles, stock, paneles...).
from controller.extra_routes import include_extra_routes  # noqa: E402

include_extra_routes(app)


@app.get("/api/health", tags=["health"])
async def health() -> JSONResponse:
    """Comprueba que el servidor y la base de datos responden."""
    database_ok = False
    try:
        from model.dao.firebase.firebaseDAOFactory import get_connector

        connector = get_connector()
        database_ok = connector.get_db() is not None
    except Exception as exc:
        logger.warning("Healthcheck de base de datos fallido: %s", exc)

    status_code = 200 if database_ok else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success" if database_ok else "degraded",
            "message": "Servidor funcionando correctamente" if database_ok else "Base de datos no disponible",
            "database": "ok" if database_ok else "unavailable",
        },
    )


@app.get("/", include_in_schema=False)
async def root():
    """Redirige al index del frontend si está montado; si no, muestra la API."""
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        from fastapi.responses import FileResponse

        return FileResponse(index)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Subsonic Fest API",
            "docs": "/docs",
            "health": "/api/health",
        },
    )


# El frontend se monta al final para no interceptar las rutas /api/*.
if Path(FRONTEND_DIR).is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
