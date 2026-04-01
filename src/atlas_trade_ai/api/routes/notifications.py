from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse
from atlas_trade_ai.schemas.notification import (
    DingTalkNotificationRequest,
    DingTalkNotificationResponse,
)

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.post("/dingtalk", response_model=ApiResponse[DingTalkNotificationResponse])
def send_dingtalk(
    request: DingTalkNotificationRequest,
) -> ApiResponse[DingTalkNotificationResponse]:
    result = container.notification_service.send_dingtalk(request.model_dump())
    return ApiResponse(data=DingTalkNotificationResponse(**result))
