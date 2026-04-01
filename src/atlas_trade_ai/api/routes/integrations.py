from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse
from atlas_trade_ai.schemas.integration import AdapterHealthRead, IntegrationSnapshotRead

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("", response_model=ApiResponse[list[AdapterHealthRead]])
def list_integrations() -> ApiResponse[list[AdapterHealthRead]]:
    items = [AdapterHealthRead(**item) for item in container.integration_service.list_adapter_health()]
    return ApiResponse(data=items)


@router.get("/crm", response_model=ApiResponse[list[IntegrationSnapshotRead]])
def get_crm_snapshot() -> ApiResponse[list[IntegrationSnapshotRead]]:
    snapshot = container.integration_service.get_crm_snapshot()
    return ApiResponse(
        data=[IntegrationSnapshotRead(section=key, items=value) for key, value in snapshot.items()]
    )


@router.get("/erp", response_model=ApiResponse[list[IntegrationSnapshotRead]])
def get_erp_snapshot() -> ApiResponse[list[IntegrationSnapshotRead]]:
    snapshot = container.integration_service.get_erp_snapshot()
    return ApiResponse(
        data=[IntegrationSnapshotRead(section=key, items=value) for key, value in snapshot.items()]
    )


@router.get("/dingtalk", response_model=ApiResponse[list[IntegrationSnapshotRead]])
def get_dingtalk_snapshot() -> ApiResponse[list[IntegrationSnapshotRead]]:
    snapshot = container.integration_service.get_dingtalk_snapshot()
    return ApiResponse(
        data=[IntegrationSnapshotRead(section=key, items=value) for key, value in snapshot.items()]
    )
