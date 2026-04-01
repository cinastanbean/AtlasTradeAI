from __future__ import annotations

from atlas_trade_ai.core.store import SQLiteStore
from atlas_trade_ai.services.order_service import OrderService


class ContextBuilderService:
    def __init__(self, store: SQLiteStore, order_service: OrderService) -> None:
        self.store = store
        self.order_service = order_service

    def build_follow_up_context(self, payload: dict) -> dict:
        order = self.order_service.get_order(payload["order_id"])
        customer = self.store.get_customer(order["customer_id"])
        related_exceptions = [
            item
            for item in self.store.list_exceptions()
            if item.get("related_order_id") == payload["order_id"]
        ]
        return {
            "trigger_event": {
                "event_id": payload["event_id"],
                "event_type": payload["event_type"],
                "event_time": payload["event_time"],
                "source_system": payload["source_system"],
                "biz_object_type": payload["biz_object_type"],
                "biz_object_id": payload["biz_object_id"],
            },
            "order_context": {
                "order_id": order["order_id"],
                "order_no": order["order_no"],
                "current_status": order["current_status"],
                "sub_status": order.get("sub_status"),
                "risk_level": order.get("risk_level", "low"),
                "planned_delivery_date": order.get("planned_delivery_date"),
                "payment_status": order.get("payment_status"),
            },
            "customer_context": {
                "customer_id": customer["customer_id"],
                "customer_name": customer["customer_name"],
                "customer_level": customer.get("customer_level", "普通客户"),
                "business_type": customer["business_type"],
                "owner_id": customer.get("owner_id"),
            },
            "fulfillment_context": {
                "milestones": order.get("milestones", []),
                "latest_logistics_status": order.get("logistics_status"),
                "document_status": order.get("document_status"),
                "customs_status": order.get("customs_status"),
                "exceptions": related_exceptions,
            },
            "payment_context": {
                "receivable_amount": order.get("total_amount") or payload.get("payload", {}).get("receivable_amount", 0.0),
                "received_amount": payload.get("payload", {}).get("received_amount", 0.0),
                "due_date": payload.get("payload", {}).get("due_date"),
                "overdue_days": payload.get("payload", {}).get("overdue_days", 0),
            },
        }
