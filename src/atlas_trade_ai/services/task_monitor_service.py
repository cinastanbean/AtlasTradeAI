from __future__ import annotations

from atlas_trade_ai.core.config_loader import JsonConfigLoader
from atlas_trade_ai.core.store import SQLiteStore


class TaskMonitorService:
    def __init__(self, store: SQLiteStore, loader: JsonConfigLoader) -> None:
        self.store = store
        org = loader.load("organization_directory.json")
        self.users = {item["user_id"]: item for item in org.get("users", [])}

    def get_owner_view(self) -> dict:
        tasks = self.store.list_tasks()
        open_tasks = [item for item in tasks if item.get("task_status") != "已完成"]
        escalation_tasks = [
            item
            for item in open_tasks
            if item.get("task_type") in {"order_orchestrator_escalation", "sla_breach_escalation"}
        ]
        by_owner: dict[str, dict] = {}
        for task in open_tasks:
            assignee_id = task.get("assignee_id") or "unassigned"
            owner = by_owner.setdefault(
                assignee_id,
                {
                    "assignee_id": assignee_id,
                    "assignee_name": self.users.get(assignee_id, {}).get("name", assignee_id),
                    "role": self.users.get(assignee_id, {}).get("role", "未分配"),
                    "pending_count": 0,
                    "high_priority_count": 0,
                    "escalation_task_count": 0,
                    "tasks": [],
                },
            )
            owner["pending_count"] += 1
            if task.get("priority") == "high":
                owner["high_priority_count"] += 1
            if task.get("task_type") in {"order_orchestrator_escalation", "sla_breach_escalation"}:
                owner["escalation_task_count"] += 1
            owner["tasks"].append(task)

        owners = sorted(
            by_owner.values(),
            key=lambda item: (-item["escalation_task_count"], -item["high_priority_count"], item["assignee_name"]),
        )
        return {
            "owner_count": len(owners),
            "open_task_count": len(open_tasks),
            "escalation_task_count": len(escalation_tasks),
            "owners": owners,
            "escalation_tasks": escalation_tasks[:20],
        }
