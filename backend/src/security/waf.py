"""Middleware WAF con límite de peticiones por IP (TK-016-1)."""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from security.rate_limiter import client_ip, limit_for_path, limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Aplica 10 req/min a /api/auth y 100 req/min al resto de la API."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not path.startswith("/api/"):
            return await call_next(request)

        ip = client_ip(request)
        limit = limit_for_path(path)
        allowed, retry_after = limiter.allow(f"{ip}:{limit}", limit)
        if not allowed:
            print(f"[WAF] IP bloqueada temporalmente: {ip} ({path})")
            return JSONResponse(
                status_code=429,
                content={"status": "error", "detail": "Demasiadas peticiones. Inténtalo más tarde."},
                headers={"Retry-After": str(retry_after)},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        return response
