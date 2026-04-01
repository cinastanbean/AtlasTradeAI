from __future__ import annotations

from datetime import datetime, timedelta

from atlas_trade_ai.core.store import SQLiteStore


class WorkbenchService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def get_summary(self) -> dict:
        customers = self.store.list_customers()
        orders = self.store.list_orders()
        tasks = self.store.list_tasks()
        exceptions = self.store.list_exceptions()
        events = self.store.list_events()
        agent_runs = self.store.list_agent_runs()
        notifications = self.store.list_notifications()
        high_risk_orders = [item for item in orders if item.get("risk_level") in {"high", "medium"}]
        pending_tasks = [item for item in tasks if item.get("task_status") == "待处理"]
        open_exceptions = [item for item in exceptions if item.get("exception_status") != "已解决"]
        escalated_orders = []
        sla_overdue_orders = []
        for order in orders:
            last_orchestration = order.get("last_orchestration") or {}
            escalation = last_orchestration.get("escalation") or {}
            if escalation.get("required"):
                escalated_orders.append(
                    {
                        "order_id": order["order_id"],
                        "order_no": order["order_no"],
                        "current_status": order.get("current_status"),
                        "risk_level": escalation.get("level"),
                    }
                )
            if escalation.get("required") and last_orchestration.get("sla_hours") and last_orchestration.get("event_time"):
                due_at = datetime.fromisoformat(last_orchestration["event_time"]) + timedelta(
                    hours=last_orchestration["sla_hours"]
                )
                if datetime.now().astimezone() > due_at:
                    sla_overdue_orders.append(order)
        return {
            "customer_count": len(customers),
            "order_count": len(orders),
            "pending_task_count": len(pending_tasks),
            "open_exception_count": len(open_exceptions),
            "event_count": len(events),
            "agent_run_count": len(agent_runs),
            "escalated_order_count": len(escalated_orders),
            "sla_overdue_count": len(sla_overdue_orders),
            "high_risk_orders": high_risk_orders[:5],
            "escalated_orders": escalated_orders[:5],
            "latest_tasks": pending_tasks[:5],
            "latest_exceptions": open_exceptions[:5],
            "latest_agent_runs": agent_runs[:5],
            "latest_notifications": notifications[:5],
        }
