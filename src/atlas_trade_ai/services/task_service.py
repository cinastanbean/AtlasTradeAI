from __future__ import annotations

from datetime import datetime

from atlas_trade_ai.adapters.dingtalk import DingTalkAdapter
from atlas_trade_ai.core.store import SQLiteStore


class TaskService:
    def __init__(self, store: SQLiteStore, dingtalk_adapter: DingTalkAdapter | None = None) -> None:
        self.store = store
        self.dingtalk_adapter = dingtalk_adapter

    def create_task(self, payload: dict) -> dict:
        existing = self.find_open_task(
            task_type=payload["task_type"],
            related_order_id=payload.get("related_order_id"),
            assignee_id=payload.get("assignee_id"),
            task_title=payload.get("task_title"),
        )
        if existing is not None:
            return existing
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
        if self.dingtalk_adapter is not None:
            try:
                todo = self.dingtalk_adapter.create_todo(
                    {
                        "subject": item["task_title"],
                        "description": item.get("task_description"),
                        "assigneeId": item.get("assignee_id"),
                        "sourceId": item["task_id"],
                    }
                )
                item["dingtalk_todo"] = todo
            except Exception as exc:  # noqa: BLE001
                item["dingtalk_todo"] = {"success": False, "error": str(exc)}
        return self.store.save_task(item)

    def find_open_task(
        self,
        task_type: str,
        related_order_id: str | None = None,
        assignee_id: str | None = None,
        task_title: str | None = None,
    ) -> dict | None:
        for item in self.store.list_tasks():
            if item.get("task_status") != "待处理":
                continue
            if item.get("task_type") != task_type:
                continue
            if related_order_id is not None and item.get("related_order_id") != related_order_id:
                continue
            if assignee_id is not None and item.get("assignee_id") != assignee_id:
                continue
            if task_title is not None and item.get("task_title") != task_title:
                continue
            return item
        return None

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

    def update_task_status(self, task_id: str, task_status: str, operator: str | None = None) -> dict:
        item = next(task for task in self.store.list_tasks() if task["task_id"] == task_id)
        item["task_status"] = task_status
        item["updated_by"] = operator
        item["updated_at"] = datetime.now().astimezone().isoformat()
        return self.store.save_task(item)
