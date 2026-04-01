from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.agent_run import AgentRunRead
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/agent-runs", tags=["agent-runs"])


@router.get("", response_model=ApiResponse[list[AgentRunRead]])
def list_agent_runs(agent_name: str | None = Query(default=None)) -> ApiResponse[list[AgentRunRead]]:
    items = [AgentRunRead(**item) for item in container.agent_run_service.list_runs(agent_name)]
    return ApiResponse(data=items)
