from __future__ import annotations

from atlas_trade_ai.core.store import SQLiteStore


class OrderService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def list_orders(self, status: str | None = None) -> list[dict]:
        items = self.store.list_orders()
        if status:
            items = [item for item in items if item["current_status"] == status]
        return items

    def get_order(self, order_id: str) -> dict:
        return self.store.get_order(order_id)

    def update_status(
        self,
        order_id: str,
        status_after: str,
        sub_status: str | None,
    ) -> dict:
        order = self.store.get_order(order_id)
        previous = order["current_status"]
        order["current_status"] = status_after
        order["sub_status"] = sub_status
        self.store.save_order(order)
        return {
            "order_id": order_id,
            "status_before": previous,
            "status_after": status_after,
            "sub_status": sub_status,
        }
