from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse
from atlas_trade_ai.schemas.workbench import WorkbenchSummary

router = APIRouter(prefix="/api/workbench", tags=["workbench"])


@router.get("/summary", response_model=ApiResponse[WorkbenchSummary])
def get_workbench_summary() -> ApiResponse[WorkbenchSummary]:
    return ApiResponse(data=WorkbenchSummary(**container.workbench_service.get_summary()))
