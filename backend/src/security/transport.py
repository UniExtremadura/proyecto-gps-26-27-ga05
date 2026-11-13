"""Redirección HTTPS, CORS y cabeceras de seguridad (TK-017-2)."""
import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

FORCE_HTTPS = os.getenv("FORCE_HTTPS", "False") == "True"
HSTS_MAX_AGE = int(os.getenv("HSTS_MAX_AGE", 31536000))

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "style-src 'self' 'unsafe-inline' https:; "
        "script-src 'self' 'unsafe-inline' https:; "
        "connect-src 'self' https: http:; "
        "frame-ancestors 'none'"
    ),
}


class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """Redirige HTTP a HTTPS con 301 cuando FORCE_HTTPS está activo."""

    async def dispatch(self, request, call_next):
        if FORCE_HTTPS and request.url.scheme != "https":
            forwarded = request.headers.get("x-forwarded-proto", "http")
            if forwarded != "https":
                secure_url = request.url.replace(scheme="https")
                return RedirectResponse(url=str(secure_url), status_code=301)
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Añade cabeceras de protección a todas las respuestas."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers.setdefault(header, value)
        if request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https":
            response.headers.setdefault("Strict-Transport-Security", f"max-age={HSTS_MAX_AGE}; includeSubDomains")
        return response
