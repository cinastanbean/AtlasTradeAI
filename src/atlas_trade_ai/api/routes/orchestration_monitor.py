from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/workbench", tags=["workbench"])


@router.get("/escalations", response_model=ApiResponse[list[dict]])
def list_escalations() -> ApiResponse[list[dict]]:
    return ApiResponse(data=container.orchestration_monitor_service.list_escalated_orders())


@router.get("/composite-risks", response_model=ApiResponse[list[dict]])
def get_composite_risks() -> ApiResponse[list[dict]]:
    return ApiResponse(data=container.orchestration_monitor_service.get_composite_risk_stats())
