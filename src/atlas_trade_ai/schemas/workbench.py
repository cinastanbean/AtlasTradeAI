from __future__ import annotations

from pydantic import BaseModel


class WorkbenchItem(BaseModel):
    order_id: str | None = None
    order_no: str | None = None
    current_status: str | None = None
    risk_level: str | None = None
    task_id: str | None = None
    task_title: str | None = None
    priority: str | None = None
    exception_id: str | None = None
    exception_type: str | None = None
    exception_level: str | None = None


class WorkbenchSummary(BaseModel):
    customer_count: int
    order_count: int
    pending_task_count: int
    open_exception_count: int
    event_count: int
    high_risk_orders: list[WorkbenchItem]
    latest_tasks: list[WorkbenchItem]
    latest_exceptions: list[WorkbenchItem]
