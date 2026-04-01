from __future__ import annotations

from datetime import datetime

from atlas_trade_ai.core.store import SQLiteStore


class TaskService:
    def __init__(self, store: SQLiteStore) -> None:
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
            "created_at": datetime.now().astimezone().isoformat(),
        }
        return self.store.save_task(item)

    def list_tasks(
        self,
        assignee_id: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        items = self.store.list_tasks()
        if assignee_id:
            items = [item for item in items if item.get("assignee_id") == assignee_id]
        if status:
            items = [item for item in items if item["task_status"] == status]
        return items
