"""Middleware de validación de payloads (TK-016-2)."""
import json

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from security.sanitizer import contains_dangerous_payload

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Rechaza payloads con scripts o patrones de inyección SQL."""

    async def dispatch(self, request: Request, call_next):
        if request.method not in SAFE_METHODS:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                body = await request.body()
                if body:
                    try:
                        payload = json.loads(body)
                    except (ValueError, UnicodeDecodeError):
                        return JSONResponse(
                            status_code=400,
                            content={"status": "error", "detail": "JSON no válido"},
                        )
                    if contains_dangerous_payload(payload):
                        print(f"[SECURITY] Payload peligroso bloqueado en {request.url.path}")
                        return JSONResponse(
                            status_code=400,
                            content={"status": "error", "detail": "La entrada contiene contenido no permitido"},
                        )
        return await call_next(request)
