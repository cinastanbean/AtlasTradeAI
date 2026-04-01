from __future__ import annotations

from datetime import datetime, timedelta

from atlas_trade_ai.core.store import SQLiteStore
from atlas_trade_ai.services.notification_service import NotificationService
from atlas_trade_ai.services.task_service import TaskService


class SlaMonitorService:
    def __init__(
        self,
        store: SQLiteStore,
        task_service: TaskService,
        notification_service: NotificationService,
    ) -> None:
        self.store = store
        self.task_service = task_service
        self.notification_service = notification_service

    def scan(self, now_iso: str | None = None) -> list[dict]:
        if now_iso:
            normalized = now_iso.replace(" ", "+") if "+" not in now_iso and now_iso.count(" ") == 1 else now_iso
            now = datetime.fromisoformat(normalized)
        else:
            now = datetime.now().astimezone()
        overdue_items: list[dict] = []
        for order in self.store.list_orders():
            orchestration = order.get("last_orchestration") or {}
            if not orchestration:
                continue
            sla_hours = orchestration.get("sla_hours")
            event_time = orchestration.get("event_time")
            escalation = orchestration.get("escalation") or {}
            if not sla_hours or not event_time or not escalation.get("required"):
                continue
            due_at = datetime.fromisoformat(event_time) + timedelta(hours=sla_hours)
            if now <= due_at:
                continue
            overdue_hours = round((now - due_at).total_seconds() / 3600, 2)
            item = {
                "order_id": order["order_id"],
                "order_no": order["order_no"],
                "due_at": due_at.isoformat(),
                "overdue_hours": overdue_hours,
                "escalation_level": escalation.get("level"),
                "next_owner_agent": orchestration.get("next_owner_agent"),
                "resolved_targets": escalation.get("resolved_targets", []),
            }
            overdue_items.append(item)
            self._ensure_actions(order, orchestration, item)
        overdue_items.sort(key=lambda item: item["overdue_hours"], reverse=True)
        return overdue_items

    def _ensure_actions(self, order: dict, orchestration: dict, item: dict) -> None:
        for target in item["resolved_targets"]:
            self.task_service.create_task(
                {
                    "task_type": "sla_breach_escalation",
                    "task_title": f"SLA 超时处理：{order['order_no']}",
                    "task_description": f"订单已超过编排 SLA {item['overdue_hours']} 小时，需要立即跟进。",
                    "related_order_id": order["order_id"],
                    "assignee_id": target.get("user_id"),
                    "priority": "high",
                    "due_time": "立即处理",
                }
            )
        receiver_ids = [target["user_id"] for target in item["resolved_targets"] if target.get("user_id")]
        if receiver_ids:
            self.notification_service.send_dingtalk(
                {
                    "template_code": "ORCH_SLA_BREACH",
                    "receiver_ids": receiver_ids,
                    "payload": {
                        "order_no": order["order_no"],
                        "message": f"订单 {order['order_no']} 已超出 SLA {item['overdue_hours']} 小时。",
                        "next_owner_agent": orchestration.get("next_owner_agent"),
                    },
                }
            )
