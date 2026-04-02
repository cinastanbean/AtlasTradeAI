from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/owners", response_model=ApiResponse[dict])
def get_owner_view() -> ApiResponse[dict]:
    return ApiResponse(data=container.task_monitor_service.get_owner_view())
