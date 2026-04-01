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
    stages: list[OrderProgressStageRead]
