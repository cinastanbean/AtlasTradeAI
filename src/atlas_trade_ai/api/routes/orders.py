from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse, PageData
from atlas_trade_ai.schemas.order import (
    OrderRead,
    OrderStatusUpdateRequest,
    OrderStatusUpdateResponse,
)

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("", response_model=ApiResponse[PageData[OrderRead]])
def list_orders(
    page: int = 1,
    page_size: int = 20,
    status: str | None = Query(default=None),
) -> ApiResponse[PageData[OrderRead]]:
    items = [OrderRead(**item) for item in container.order_service.list_orders(status)]
    return ApiResponse(
        data=PageData(items=items, total=len(items), page=page, page_size=page_size)
    )


@router.get("/{order_id}", response_model=ApiResponse[OrderRead])
def get_order(order_id: str) -> ApiResponse[OrderRead]:
    return ApiResponse(data=OrderRead(**container.order_service.get_order(order_id)))


@router.post("/{order_id}/status", response_model=ApiResponse[OrderStatusUpdateResponse])
def update_order_status(
    order_id: str,
    request: OrderStatusUpdateRequest,
) -> ApiResponse[OrderStatusUpdateResponse]:
    result = container.order_service.update_status(
        order_id=order_id,
        status_after=request.status_after,
        sub_status=request.sub_status,
    )
    return ApiResponse(data=OrderStatusUpdateResponse(**result))
