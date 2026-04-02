from __future__ import annotations

from datetime import datetime

from atlas_trade_ai.adapters.dingtalk import DingTalkAdapter
from atlas_trade_ai.core.store import SQLiteStore


class NotificationService:
    def __init__(self, store: SQLiteStore, dingtalk_adapter: DingTalkAdapter | None = None) -> None:
        self.store = store
        self.dingtalk_adapter = dingtalk_adapter

    def send_dingtalk(self, payload: dict) -> dict:
        delivery = None
        if self.dingtalk_adapter is not None:
            try:
                delivery = self.dingtalk_adapter.send_message(payload)
            except Exception as exc:  # noqa: BLE001
                delivery = {"success": False, "mode": "adapter-error", "error": str(exc)}
        notification_id = self.store.next_id("notification")
        item = {
            "notification_id": notification_id,
            "channel": "dingtalk",
            "template_code": payload["template_code"],
            "receiver_ids": payload["receiver_ids"],
            "payload": payload["payload"],
            "sent": delivery.get("success", True) if delivery else True,
            "delivery": delivery,
            "created_at": datetime.now().astimezone().isoformat(),
        }
        return self.store.save_notification(item)
