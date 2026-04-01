from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse
from atlas_trade_ai.schemas.order_progress import OrderProgressRead

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/{order_id}/progress", response_model=ApiResponse[OrderProgressRead])
def get_order_progress(order_id: str) -> ApiResponse[OrderProgressRead]:
    return ApiResponse(data=OrderProgressRead(**container.order_progress_service.get_progress(order_id)))
