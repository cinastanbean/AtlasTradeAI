from __future__ import annotations

from atlas_trade_ai.core.store import InMemoryStore


def build_seed_store() -> InMemoryStore:
    store = InMemoryStore()

    store.customers["cus_001"] = {
        "customer_id": "cus_001",
        "customer_name": "华东重点客户A",
        "customer_level": "重点客户",
        "business_type": "内销",
        "country_or_region": "中国",
        "payment_terms": "月结30天",
        "owner_id": "user_sales_01",
        "contacts": [
            {
                "contact_id": "ct_001",
                "contact_name": "张三",
                "phone": "13800000000",
            }
        ],
    }

    store.orders["ord_001"] = {
        "order_id": "ord_001",
        "order_no": "SO-2026-0001",
        "customer_id": "cus_001",
        "customer_name": "华东重点客户A",
        "business_type": "内销",
        "current_status": "执行中",
        "sub_status": "生产中",
        "risk_level": "medium",
        "planned_delivery_date": "2026-04-10",
        "payment_status": "待回款",
        "milestones": [
            {
                "milestone_type": "生产完成",
                "planned_time": "2026-04-05T18:00:00+08:00",
                "actual_time": None,
                "milestone_status": "delayed",
                "is_overdue": True,
            }
        ],
    }

    return store
