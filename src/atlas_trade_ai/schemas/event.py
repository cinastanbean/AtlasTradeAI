from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class EventCreateRequest(BaseModel):
    event_id: str | None = None
    event_type: str
    event_time: str
    source_system: str
    source_record_id: str | None = None
    biz_object_type: str
    biz_object_id: str
    order_id: str | None = None
    customer_id: str | None = None
    owner_id: str | None = None
    priority: str | None = None
    risk_level: str | None = None
    payload: dict[str, Any] = {}


class EventRead(BaseModel):
    event_id: str
    event_type: str
    event_time: str
    priority: str | None = None


class EventWriteResponse(BaseModel):
    event_id: str
    accepted: bool
    matched_rule: str | None = None
    orchestration: dict[str, Any] | None = None
    generated_task_ids: list[str] = []
    generated_exception_ids: list[str] = []
    notification_ids: list[str] = []
