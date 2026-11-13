"""Registro centralizado de routers añadidos de forma incremental."""
from fastapi import FastAPI

from security.waf import RateLimitMiddleware
from security.input_guard import InputSanitizationMiddleware
from security.transport import HTTPSRedirectMiddleware, SecurityHeadersMiddleware

from controller.routers.core_routes import router as core_router
from controller.routers.auth_routes import router as auth_router
from controller.routers.rbac_routes import router as rbac_router
from controller.routers.oauth_routes import router as oauth_router
from controller.routers.catalog_routes import router as catalog_router
from controller.routers.event_admin_routes import router as event_admin_router
from controller.routers.booking_routes import router as booking_router
from controller.routers.admin_moderation_routes import router as admin_moderation_router
from controller.routers.profile_routes import router as profile_router
from controller.routers.stock_routes import router as stock_router
from controller.routers.metrics_routes import router as metrics_router
from controller.routers.password_reset_routes import router as password_reset_router
from controller.routers.analytics_routes import router as analytics_router


def include_extra_routes(app: FastAPI) -> None:
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(InputSanitizationMiddleware)
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.include_router(auth_router)
    app.include_router(rbac_router)
    app.include_router(core_router)
    app.include_router(oauth_router)
    app.include_router(catalog_router)
    app.include_router(event_admin_router)
    app.include_router(booking_router)
    app.include_router(admin_moderation_router)
    app.include_router(profile_router)
    app.include_router(stock_router)
    app.include_router(metrics_router)
    app.include_router(password_reset_router)
    app.include_router(analytics_router)
