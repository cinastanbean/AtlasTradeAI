from __future__ import annotations

from atlas_trade_ai.core.store import InMemoryStore


class WorkbenchService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def get_summary(self) -> dict:
        high_risk_orders = [
            item for item in self.store.orders.values() if item.get("risk_level") in {"high", "medium"}
        ]
        pending_tasks = [
            item for item in self.store.tasks.values() if item.get("task_status") == "待处理"
        ]
        open_exceptions = [
            item
            for item in self.store.exceptions.values()
            if item.get("exception_status") != "已解决"
        ]
        return {
            "customer_count": len(self.store.customers),
            "order_count": len(self.store.orders),
            "pending_task_count": len(pending_tasks),
            "open_exception_count": len(open_exceptions),
            "event_count": len(self.store.events),
            "high_risk_orders": high_risk_orders[:5],
            "latest_tasks": pending_tasks[:5],
            "latest_exceptions": open_exceptions[:5],
        }
