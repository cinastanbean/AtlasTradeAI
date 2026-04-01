from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse, PageData
from atlas_trade_ai.schemas.event import EventCreateRequest, EventRead, EventWriteResponse

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("", response_model=ApiResponse[EventWriteResponse])
def create_event(request: EventCreateRequest) -> ApiResponse[EventWriteResponse]:
    result = container.event_service.write_event(request.model_dump())
    return ApiResponse(data=EventWriteResponse(**result))


@router.get("", response_model=ApiResponse[PageData[EventRead]])
def list_events(
    order_id: str | None = Query(default=None),
    page: int = 1,
    page_size: int = 20,
) -> ApiResponse[PageData[EventRead]]:
    items = [EventRead(**item) for item in container.event_service.list_events(order_id=order_id)]
    return ApiResponse(
        data=PageData(items=items, total=len(items), page=page, page_size=page_size)
    )
