from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse
from atlas_trade_ai.schemas.integration import AdapterHealthRead

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("", response_model=ApiResponse[list[AdapterHealthRead]])
def list_integrations() -> ApiResponse[list[AdapterHealthRead]]:
    items = [AdapterHealthRead(**item) for item in container.integration_service.list_adapter_health()]
    return ApiResponse(data=items)
