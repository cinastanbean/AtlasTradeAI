from __future__ import annotations

from fastapi import APIRouter, HTTPException

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.agent import FollowUpAgentRunRequest, FollowUpAgentRunResponse
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("/follow-up/run", response_model=ApiResponse[FollowUpAgentRunResponse])
def run_follow_up_agent(
    request: FollowUpAgentRunRequest,
) -> ApiResponse[FollowUpAgentRunResponse]:
    result = container.follow_up_agent_service.run(request.model_dump())
    return ApiResponse(data=FollowUpAgentRunResponse(**result))


@router.post("/{agent_key}/run", response_model=ApiResponse[FollowUpAgentRunResponse])
def run_agent(
    agent_key: str,
    request: FollowUpAgentRunRequest,
) -> ApiResponse[FollowUpAgentRunResponse]:
    agent_service = container.agent_registry_service.get_agent_service(agent_key)
    if agent_service is None:
        raise HTTPException(status_code=404, detail=f"Agent {agent_key} 不存在")
    result = agent_service.run(request.model_dump())
    return ApiResponse(data=FollowUpAgentRunResponse(**result))
