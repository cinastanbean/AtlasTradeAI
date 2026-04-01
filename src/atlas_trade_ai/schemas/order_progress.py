from __future__ import annotations

from pydantic import BaseModel


class OrderProgressStageRead(BaseModel):
    layer: str
    status: str
    state: str


class OrderProgressRead(BaseModel):
    order_id: str
    order_no: str
    current_status: str
    current_layer: str | None = None
    next_owner_agent: str | None = None
    blocked: bool = False
    sla_hours: int | None = None
    escalation: dict | None = None
    stages: list[OrderProgressStageRead]
