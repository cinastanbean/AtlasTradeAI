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


class TaskStatusUpdateRequest(BaseModel):
    task_status: str
    operator: str | None = None


class TaskRead(BaseModel):
    task_id: str
    task_type: str | None = None
    task_title: str
    task_description: str | None = None
    assignee_id: str | None = None
    priority: str
    due_time: str | None = None
    task_status: str
    created_at: str | None = None
    related_order_id: str | None = None
