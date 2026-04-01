from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.agent_catalog import AgentCatalogRead
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("/catalog", response_model=ApiResponse[list[AgentCatalogRead]])
def list_agent_catalog() -> ApiResponse[list[AgentCatalogRead]]:
    items = [AgentCatalogRead(**item) for item in container.agent_registry_service.list_agents()]
    return ApiResponse(data=items)
