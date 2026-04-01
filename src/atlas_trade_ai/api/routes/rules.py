from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.get("/events", response_model=ApiResponse[list[dict]])
def list_event_catalog() -> ApiResponse[list[dict]]:
    return ApiResponse(data=container.rule_registry_service.list_events())


@router.get("/workflow", response_model=ApiResponse[list[dict]])
def list_workflow_rules() -> ApiResponse[list[dict]]:
    return ApiResponse(data=container.rule_registry_service.list_rules())
