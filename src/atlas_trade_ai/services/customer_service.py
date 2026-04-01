from __future__ import annotations

from atlas_trade_ai.core.store import SQLiteStore


class CustomerService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def list_customers(self, keyword: str | None = None) -> list[dict]:
        items = self.store.list_customers()
        if keyword:
            items = [item for item in items if keyword in item["customer_name"]]
        return items

    def get_customer(self, customer_id: str) -> dict:
        return self.store.get_customer(customer_id)
