from __future__ import annotations

from atlas_trade_ai.core.store import InMemoryStore


class NotificationService:
    def __init__(self, store: InMemoryStore) -> None:
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
        }
        self.store.notifications.append(item)
        return item
