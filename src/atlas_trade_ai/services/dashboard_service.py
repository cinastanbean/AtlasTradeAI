from __future__ import annotations

from atlas_trade_ai.core.store import SQLiteStore


class DashboardService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def get_order_detail_dashboard(self, order_id: str) -> dict:
        order = self.store.get_order(order_id)
        customer = self.store.get_customer(order["customer_id"])
        tasks = [item for item in self.store.list_tasks() if item.get("related_order_id") == order_id]
        exceptions = [
            item for item in self.store.list_exceptions() if item.get("related_order_id") == order_id
        ]
        events = [item for item in self.store.list_events() if item.get("order_id") == order_id]
        agent_runs = [
            item for item in self.store.list_agent_runs() if item.get("order_id") == order_id
        ]
        return {
            "order": order,
            "customer": customer,
            "tasks": tasks,
            "exceptions": exceptions,
            "events": sorted(events, key=lambda item: item.get("event_time", ""), reverse=True),
            "agent_runs": agent_runs,
        }
