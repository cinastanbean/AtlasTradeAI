from __future__ import annotations

from pydantic import BaseModel


class TaskCreateRequest(BaseModel):
    task_type: str
    task_title: str
    task_description: str | None = None
    related_order_id: str | None = None
    assignee_id: str | None = None
    priority: str = "medium"
    due_time: str | None = None


class TaskRead(BaseModel):
    task_id: str
    task_title: str
    priority: str
    task_status: str
    related_order_id: str | None = None
