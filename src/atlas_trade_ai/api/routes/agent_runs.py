from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.agent_run import AgentRunRead
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/agent-runs", tags=["agent-runs"])


@router.get("", response_model=ApiResponse[list[AgentRunRead]])
def list_agent_runs(
    agent_name: str | None = Query(default=None),
    event_type: str | None = Query(default=None),
    order_id: str | None = Query(default=None),
    engine_provider: str | None = Query(default=None),
    limit: int | None = Query(default=None),
) -> ApiResponse[list[AgentRunRead]]:
    items = [
        AgentRunRead(**item)
        for item in container.agent_run_service.query_runs(
            agent_name=agent_name,
            event_type=event_type,
            order_id=order_id,
            engine_provider=engine_provider,
            limit=limit,
        )
    ]
    return ApiResponse(data=items)


@router.get("/{run_id}", response_model=ApiResponse[AgentRunRead])
def get_agent_run(run_id: str) -> ApiResponse[AgentRunRead]:
    return ApiResponse(data=AgentRunRead(**container.agent_run_service.get_run(run_id)))
