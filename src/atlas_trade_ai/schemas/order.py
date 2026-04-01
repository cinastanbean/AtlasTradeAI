from __future__ import annotations

from pydantic import BaseModel


class MilestoneRead(BaseModel):
    milestone_type: str
    planned_time: str | None = None
    actual_time: str | None = None
    milestone_status: str
    is_overdue: bool = False


class OrderRead(BaseModel):
    order_id: str
    order_no: str
    customer_id: str | None = None
    customer_name: str
    business_type: str
    current_status: str
    sub_status: str | None = None
    risk_level: str
    planned_delivery_date: str | None = None
    payment_status: str | None = None
    milestones: list[MilestoneRead] = []


class OrderStatusUpdateRequest(BaseModel):
    status_after: str
    sub_status: str | None = None
    operator: str
    reason: str


class OrderStatusUpdateResponse(BaseModel):
    order_id: str
    status_before: str
    status_after: str
    sub_status: str | None = None
