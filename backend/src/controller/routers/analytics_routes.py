"""API de métricas globales para administración (TK-015-1)."""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, PlainTextResponse

from security.rbac import require_roles
from services.analytics_service import global_metrics, global_metrics_csv

router = APIRouter(prefix="/api/admin/analytics", tags=["admin-analytics"])


@router.get("")
async def analytics_overview(
    days: int = Query(30, ge=0, le=365),
    user: dict = Depends(require_roles("admin")),
):
    return JSONResponse(status_code=200, content={"status": "success", "data": global_metrics(days)})


@router.get("/export")
async def analytics_export(
    days: int = Query(30, ge=0, le=365),
    user: dict = Depends(require_roles("admin")),
):
    return PlainTextResponse(
        content=global_metrics_csv(days),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=metricas-globales.csv"},
    )
