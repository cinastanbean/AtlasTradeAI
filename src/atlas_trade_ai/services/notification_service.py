from __future__ import annotations

from datetime import datetime

from atlas_trade_ai.core.store import SQLiteStore


class NotificationService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def send_dingtalk(self, payload: dict) -> dict:
        notification_id = self.store.next_id("notification")
        item = {
            "notification_id": notification_id,
            "channel": "dingtalk",
            "template_code": payload["template_code"],
            "receiver_ids": payload["receiver_ids"],
            "payload": payload["payload"],
            "sent": True,
            "created_at": datetime.now().astimezone().isoformat(),
        }
        return self.store.save_notification(item)
