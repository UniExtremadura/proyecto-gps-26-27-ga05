"""Registro centralizado de routers añadidos de forma incremental."""
from fastapi import FastAPI

from controller.routers.auth_routes import router as auth_router
from controller.routers.rbac_routes import router as rbac_router
from controller.routers.oauth_routes import router as oauth_router


def include_extra_routes(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(rbac_router)
    app.include_router(oauth_router)
