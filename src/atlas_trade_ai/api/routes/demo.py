from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse
from atlas_trade_ai.schemas.demo import DemoScenarioRead, DemoScenarioRunResponse

router = APIRouter(prefix="/api/demo", tags=["demo"])


@router.get("/scenarios", response_model=ApiResponse[list[DemoScenarioRead]])
def list_scenarios() -> ApiResponse[list[DemoScenarioRead]]:
    items = [DemoScenarioRead(**item) for item in container.demo_scenario_service.list_scenarios()]
    return ApiResponse(data=items)


@router.post("/scenarios/{code}/run", response_model=ApiResponse[DemoScenarioRunResponse])
def run_scenario(code: str) -> ApiResponse[DemoScenarioRunResponse]:
    return ApiResponse(data=DemoScenarioRunResponse(**container.demo_scenario_service.run_scenario(code)))
