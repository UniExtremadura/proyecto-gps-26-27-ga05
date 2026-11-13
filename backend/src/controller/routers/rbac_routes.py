"""Endpoints de comprobación de roles y permisos (TK-002-2)."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from model.roles import ROLE_DEFINITIONS, role_permissions
from security.rbac import get_current_user, require_permission, require_roles

router = APIRouter(prefix="/api/rbac", tags=["rbac"])


@router.get("/me")
async def rbac_me(user: dict = Depends(get_current_user)):
    """Devuelve el rol y permisos efectivos del usuario autenticado."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "user": user,
            "permissions": role_permissions(user.get("role", "")),
        },
    )


@router.get("/roles")
async def rbac_roles(user: dict = Depends(require_roles("admin"))):
    """Catálogo de roles. Solo accesible por administradores."""
    return JSONResponse(status_code=200, content={"status": "success", "data": ROLE_DEFINITIONS})


@router.get("/organizer-check")
async def organizer_check(user: dict = Depends(require_roles("gestor", "organizador", "admin"))):
    """Comprueba acceso de organizador."""
    return JSONResponse(status_code=200, content={"status": "success", "message": "Acceso de organizador permitido"})


@router.get("/moderation-check")
async def moderation_check(user: dict = Depends(require_permission("users:moderate"))):
    """Comprueba permiso de moderación."""
    return JSONResponse(status_code=200, content={"status": "success", "message": "Acceso de moderación permitido"})
