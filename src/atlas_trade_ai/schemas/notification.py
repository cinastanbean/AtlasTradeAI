from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class DingTalkNotificationRequest(BaseModel):
    template_code: str
    receiver_ids: list[str]
    payload: dict[str, Any]


class DingTalkNotificationResponse(BaseModel):
    sent: bool
    channel: str = "dingtalk"
    notification_id: str
