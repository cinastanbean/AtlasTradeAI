from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/workbench", tags=["workbench"])


@router.get("/sla-overdue", response_model=ApiResponse[list[dict]])
def list_sla_overdue(now_iso: str | None = Query(default=None)) -> ApiResponse[list[dict]]:
    return ApiResponse(data=container.sla_monitor_service.scan(now_iso=now_iso))
