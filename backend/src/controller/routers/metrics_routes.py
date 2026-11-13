"""API de métricas de ventas (TK-013-1)."""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, PlainTextResponse

from security.rbac import require_roles
from services.metrics_service import sales_csv, sales_metrics

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/sales")
async def metrics_sales(
    days: int = Query(30, ge=0, le=365),
    user: dict = Depends(require_roles("proveedor", "gestor", "admin")),
):
    provider_uid = user["uid"] if user.get("role") == "proveedor" else ""
    return JSONResponse(status_code=200, content={"status": "success", "data": sales_metrics(provider_uid, days)})


@router.get("/sales/export")
async def metrics_sales_export(
    days: int = Query(30, ge=0, le=365),
    user: dict = Depends(require_roles("proveedor", "gestor", "admin")),
):
    provider_uid = user["uid"] if user.get("role") == "proveedor" else ""
    return PlainTextResponse(
        content=sales_csv(provider_uid, days),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ventas.csv"},
    )
