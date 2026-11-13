"""API de stock (TK-011-1)."""
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from security.rbac import require_roles
from services.stock_service import decrement_stock, get_stock, list_stock, low_stock_alerts, update_stock

router = APIRouter(prefix="/api/stock", tags=["stock"])


@router.get("")
async def stock_list(user: dict = Depends(require_roles("proveedor", "gestor", "admin"))):
    return JSONResponse(status_code=200, content={"status": "success", "data": list_stock()})


@router.get("/alerts")
async def stock_alerts(user: dict = Depends(require_roles("proveedor", "gestor", "admin"))):
    return JSONResponse(status_code=200, content={"status": "success", "data": low_stock_alerts()})


@router.get("/{product_id}")
async def stock_detail(product_id: str, user: dict = Depends(require_roles("proveedor", "gestor", "admin"))):
    stock = get_stock(product_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return JSONResponse(status_code=200, content={"status": "success", "data": stock})


@router.put("/{product_id}")
async def stock_update(product_id: str, data: dict = Body(...), user: dict = Depends(require_roles("proveedor", "gestor", "admin"))):
    try:
        updated = update_stock(product_id, data.get("stock", 0), data.get("min_stock", 5))
        return JSONResponse(status_code=200, content={"status": "success", "data": updated})
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/{product_id}/decrement")
async def stock_decrement(product_id: str, data: dict = Body(default={}), user: dict = Depends(require_roles("proveedor", "gestor", "admin"))):
    try:
        updated = decrement_stock(product_id, data.get("quantity", 1))
        return JSONResponse(status_code=200, content={"status": "success", "data": updated})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
