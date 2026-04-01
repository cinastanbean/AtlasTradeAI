from __future__ import annotations

from atlas_trade_ai.core.store import InMemoryStore


class TaskService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def create_task(self, payload: dict) -> dict:
        task_id = self.store.next_id("task")
        item = {
            "task_id": task_id,
            "task_type": payload["task_type"],
            "task_title": payload["task_title"],
            "task_description": payload.get("task_description"),
            "related_order_id": payload.get("related_order_id"),
            "assignee_id": payload.get("assignee_id"),
            "priority": payload.get("priority", "medium"),
            "due_time": payload.get("due_time"),
            "task_status": "待处理",
        }
        self.store.tasks[task_id] = item
        return item

    def list_tasks(
        self,
        assignee_id: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        items = list(self.store.tasks.values())
        if assignee_id:
            items = [item for item in items if item.get("assignee_id") == assignee_id]
        if status:
            items = [item for item in items if item["task_status"] == status]
        return items
