from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse, PageData
from atlas_trade_ai.schemas.exception import ExceptionCreateRequest, ExceptionRead

router = APIRouter(prefix="/api/exceptions", tags=["exceptions"])


@router.post("", response_model=ApiResponse[ExceptionRead])
def create_exception(request: ExceptionCreateRequest) -> ApiResponse[ExceptionRead]:
    result = container.exception_service.create_exception(request.model_dump())
    return ApiResponse(data=ExceptionRead(**result))


@router.get("", response_model=ApiResponse[PageData[ExceptionRead]])
def list_exceptions(
    level: str | None = Query(default=None),
    status: str | None = Query(default=None),
    page: int = 1,
    page_size: int = 20,
) -> ApiResponse[PageData[ExceptionRead]]:
    items = [
        ExceptionRead(**item)
        for item in container.exception_service.list_exceptions(level=level, status=status)
    ]
    return ApiResponse(
        data=PageData(items=items, total=len(items), page=page, page_size=page_size)
    )
