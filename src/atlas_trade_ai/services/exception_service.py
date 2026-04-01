from __future__ import annotations

from atlas_trade_ai.core.store import InMemoryStore


class ExceptionService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def create_exception(self, payload: dict) -> dict:
        exception_id = self.store.next_id("exception")
        item = {
            "exception_id": exception_id,
            "exception_type": payload["exception_type"],
            "exception_level": payload["exception_level"],
            "related_order_id": payload.get("related_order_id"),
            "source_event_id": payload.get("source_event_id"),
            "owner_id": payload.get("owner_id"),
            "suggestion": payload.get("suggestion"),
            "exception_status": "已发现",
        }
        self.store.exceptions[exception_id] = item
        return item

    def list_exceptions(
        self,
        level: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        items = list(self.store.exceptions.values())
        if level:
            items = [item for item in items if item["exception_level"] == level]
        if status:
            items = [item for item in items if item["exception_status"] == status]
        return items
