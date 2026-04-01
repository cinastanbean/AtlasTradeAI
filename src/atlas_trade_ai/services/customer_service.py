from __future__ import annotations

from atlas_trade_ai.core.store import InMemoryStore


class CustomerService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def list_customers(self, keyword: str | None = None) -> list[dict]:
        items = list(self.store.customers.values())
        if keyword:
            items = [item for item in items if keyword in item["customer_name"]]
        return items

    def get_customer(self, customer_id: str) -> dict:
        return self.store.customers[customer_id]
