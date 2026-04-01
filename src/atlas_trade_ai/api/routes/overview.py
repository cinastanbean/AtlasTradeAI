from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse, ArchitectureOverview

router = APIRouter(prefix="/api/overview", tags=["overview"])


@router.get("/architecture", response_model=ApiResponse[ArchitectureOverview])
def get_architecture() -> ApiResponse[ArchitectureOverview]:
    return ApiResponse(data=ArchitectureOverview(**container.overview_service.get_architecture()))
