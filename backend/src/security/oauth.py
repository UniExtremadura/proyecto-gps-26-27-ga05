"""Validación de tokens externos de Google/Apple (TK-004-2)."""
from typing import Dict

import requests

from config.oauth import GOOGLE_TOKENINFO_URL


class OAuthError(Exception):
    pass


def verify_google_id_token(id_token: str) -> Dict[str, str]:
    """Valida un ID token de Google contra el endpoint tokeninfo."""
    if not id_token:
        raise OAuthError("Token de Google requerido")
    try:
        response = requests.get(GOOGLE_TOKENINFO_URL, params={"id_token": id_token}, timeout=5)
        if response.status_code != 200:
            raise OAuthError("Token de Google inválido")
        data = response.json()
        if not data.get("email"):
            raise OAuthError("El token de Google no contiene email")
        return {
            "provider": "google",
            "uid": data.get("sub") or data.get("email"),
            "email": str(data["email"]).lower(),
            "name": data.get("name") or data.get("email", "").split("@")[0],
            "picture": data.get("picture", ""),
        }
    except requests.RequestException as exc:
        raise OAuthError(f"No se pudo validar el token de Google: {exc}") from exc


def verify_apple_identity_token(identity_token: str, profile: Dict[str, str] = None) -> Dict[str, str]:
    """Valida (de forma simulada en desarrollo) un identity token de Apple."""
    if not identity_token:
        raise OAuthError("Token de Apple requerido")
    profile = profile or {}
    email = str(profile.get("email") or "").strip().lower()
    if not email:
        raise OAuthError("Apple no devolvió un email")
    return {
        "provider": "apple",
        "uid": profile.get("sub") or email,
        "email": email,
        "name": profile.get("name") or email.split("@")[0],
        "picture": "",
    }


def normalize_oauth_profile(profile: Dict[str, str]) -> Dict[str, str]:
    """Normaliza los datos mínimos de perfil que se guardan en Firestore."""
    return {
        "uid": profile.get("uid", ""),
        "email": profile.get("email", "").lower(),
        "name": profile.get("name", ""),
        "role": profile.get("role", "cliente"),
        "provider": profile.get("provider", ""),
        "profile_image_url": profile.get("picture", ""),
    }
