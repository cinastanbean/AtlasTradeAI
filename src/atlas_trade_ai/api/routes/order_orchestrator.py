from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/{order_id}/orchestration", response_model=ApiResponse[dict])
def get_order_orchestration(order_id: str) -> ApiResponse[dict]:
    dashboard = container.dashboard_service.get_order_detail_dashboard(order_id)
    return ApiResponse(data=dashboard.get("orchestration") or {})
