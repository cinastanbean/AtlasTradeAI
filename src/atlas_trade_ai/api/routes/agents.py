from __future__ import annotations

from fastapi import APIRouter

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
