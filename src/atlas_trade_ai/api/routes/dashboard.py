from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse
from atlas_trade_ai.schemas.dashboard import OrderDashboardRead

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/orders/{order_id}", response_model=ApiResponse[OrderDashboardRead])
def get_order_dashboard(order_id: str) -> ApiResponse[OrderDashboardRead]:
    return ApiResponse(data=OrderDashboardRead(**container.dashboard_service.get_order_detail_dashboard(order_id)))
