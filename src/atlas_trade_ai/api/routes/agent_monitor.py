from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("/monitor", response_model=ApiResponse[dict])
def get_agent_monitor() -> ApiResponse[dict]:
    return ApiResponse(data=container.agent_monitor_service.get_overview())
