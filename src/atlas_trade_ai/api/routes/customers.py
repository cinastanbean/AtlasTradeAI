from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse, PageData
from atlas_trade_ai.schemas.customer import CustomerRead

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("", response_model=ApiResponse[PageData[CustomerRead]])
def list_customers(
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = Query(default=None),
) -> ApiResponse[PageData[CustomerRead]]:
    items = [CustomerRead(**item) for item in container.customer_service.list_customers(keyword)]
    return ApiResponse(
        data=PageData(items=items, total=len(items), page=page, page_size=page_size)
    )


@router.get("/{customer_id}", response_model=ApiResponse[CustomerRead])
def get_customer(customer_id: str) -> ApiResponse[CustomerRead]:
    return ApiResponse(data=CustomerRead(**container.customer_service.get_customer(customer_id)))
