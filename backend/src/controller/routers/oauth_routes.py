"""Callbacks OAuth 2.0 (TK-004-2)."""
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse

from config.oauth import configured_providers, provider_is_configured
from security.oauth import OAuthError, normalize_oauth_profile, verify_apple_identity_token, verify_google_id_token
from security.tokens import create_access_token

router = APIRouter(prefix="/api/oauth", tags=["oauth"])


@router.get("/providers")
async def list_oauth_providers():
    """Lista los proveedores OAuth configurados."""
    return JSONResponse(
        status_code=200,
        content={"status": "success", "providers": configured_providers()},
    )


@router.post("/google/callback")
async def google_callback(data: dict = Body(...)):
    """Valida el ID token de Google y emite un JWT propio."""
    try:
        if data.get("demo"):
            profile = {
                "provider": "google",
                "uid": "google-demo",
                "email": "google.demo@subsonicfest.com",
                "name": "Usuario Google Demo",
                "picture": "",
                "role": data.get("role", "cliente"),
            }
        else:
            profile = verify_google_id_token(data.get("id_token") or data.get("credential") or "")
            profile["role"] = data.get("role", "cliente")
        user = normalize_oauth_profile(profile)
        token = create_access_token(user["uid"], user["role"], user["email"])
        return JSONResponse(status_code=200, content={"status": "success", "token": token, "user": user})
    except OAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


@router.post("/apple/callback")
async def apple_callback(data: dict = Body(...)):
    """Valida el identity token de Apple (simulado) y emite un JWT propio."""
    try:
        profile = verify_apple_identity_token(
            data.get("identity_token") or "",
            {"email": data.get("email"), "name": data.get("name"), "sub": data.get("sub")},
        )
        profile["role"] = data.get("role", "cliente")
        user = normalize_oauth_profile(profile)
        token = create_access_token(user["uid"], user["role"], user["email"])
        return JSONResponse(status_code=200, content={"status": "success", "token": token, "user": user})
    except OAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


@router.get("/{provider}/start")
async def oauth_start(provider: str):
    """Devuelve la URL de autorización del proveedor."""
    if not provider_is_configured(provider):
        raise HTTPException(status_code=503, detail="Proveedor OAuth no configurado")
    from config.oauth import get_provider_config

    config = get_provider_config(provider)
    query = "&".join(
        [
            f"client_id={config['client_id']}",
            "response_type=code",
            f"redirect_uri={config['redirect_uri']}",
            f"scope={' '.join(config['scopes'])}",
        ]
    )
    return JSONResponse(status_code=200, content={"status": "success", "url": f"{config['auth_url']}?{query}"})
