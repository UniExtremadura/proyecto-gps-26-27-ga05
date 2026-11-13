"""Configuración de proveedores OAuth 2.0 (TK-004-1)."""
import os

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"

APPLE_AUTH_URL = "https://appleid.apple.com/auth/authorize"
APPLE_TOKEN_URL = "https://appleid.apple.com/auth/token"

OAUTH_PROVIDERS = {
    "google": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv(
            "GOOGLE_REDIRECT_URI",
            "http://localhost:3000/#oauth-callback?provider=google",
        ),
        "scopes": ["openid", "email", "profile"],
        "auth_url": GOOGLE_AUTH_URL,
        "token_url": GOOGLE_TOKEN_URL,
    },
    "apple": {
        "client_id": os.getenv("APPLE_CLIENT_ID", ""),
        "team_id": os.getenv("APPLE_TEAM_ID", ""),
        "key_id": os.getenv("APPLE_KEY_ID", ""),
        "private_key": os.getenv("APPLE_PRIVATE_KEY", ""),
        "redirect_uri": os.getenv(
            "APPLE_REDIRECT_URI",
            "http://localhost:3000/#oauth-callback?provider=apple",
        ),
        "scopes": ["name", "email"],
        "auth_url": APPLE_AUTH_URL,
        "token_url": APPLE_TOKEN_URL,
    },
}

OAUTH_STATE_SECRET = os.getenv("OAUTH_STATE_SECRET", "subsonic-oauth-state")


def get_provider_config(provider: str) -> dict:
    """Devuelve la configuración de un proveedor o lanza KeyError."""
    key = str(provider or "").strip().lower()
    if key not in OAUTH_PROVIDERS:
        raise KeyError(f"Proveedor OAuth no soportado: {provider}")
    return OAUTH_PROVIDERS[key]


def provider_is_configured(provider: str) -> bool:
    config = get_provider_config(provider)
    return bool(config.get("client_id"))


def configured_providers() -> list:
    return [name for name in OAUTH_PROVIDERS if provider_is_configured(name)]
