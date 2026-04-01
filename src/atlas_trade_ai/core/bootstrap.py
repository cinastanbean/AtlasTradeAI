from __future__ import annotations

from pathlib import Path

from atlas_trade_ai.core.store import SQLiteStore


def build_seed_payload() -> dict[str, list[dict]]:
    customers = [
        {
            "customer_id": "cus_001",
            "customer_name": "华东重点客户A",
            "customer_level": "重点客户",
            "business_type": "内销",
            "country_or_region": "中国",
            "payment_terms": "月结30天",
            "owner_id": "user_sales_01",
            "contacts": [
                {"contact_id": "ct_001", "contact_name": "张三", "phone": "13800000000"}
            ],
        },
        {
            "customer_id": "cus_002",
            "customer_name": "德国外贸客户B",
            "customer_level": "战略客户",
            "business_type": "外贸",
            "country_or_region": "德国",
            "payment_terms": "TT 30/70",
            "owner_id": "user_sales_02",
            "contacts": [
                {"contact_id": "ct_002", "contact_name": "Anna", "phone": None}
            ],
        },
        {
            "customer_id": "cus_003",
            "customer_name": "美国渠道客户C",
            "customer_level": "普通客户",
            "business_type": "外贸",
            "country_or_region": "美国",
            "payment_terms": "OA 45天",
            "owner_id": "user_sales_03",
            "contacts": [
                {"contact_id": "ct_003", "contact_name": "Michael", "phone": None}
            ],
        },
        {
            "customer_id": "cus_004",
            "customer_name": "华南电商客户D",
            "customer_level": "成长客户",
            "business_type": "内销",
            "country_or_region": "中国",
            "payment_terms": "预付款",
            "owner_id": "user_sales_01",
            "contacts": [
                {"contact_id": "ct_004", "contact_name": "李四", "phone": "13900000000"}
            ],
        },
    ]

    orders = [
        {
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
            "currency": "CNY",
            "total_amount": 128000.0,
            "milestones": [
                {
                    "milestone_type": "排产确认",
                    "planned_time": "2026-04-01T10:00:00+08:00",
                    "actual_time": "2026-04-01T09:30:00+08:00",
                    "milestone_status": "completed",
                    "is_overdue": False,
                },
                {
                    "milestone_type": "生产完成",
                    "planned_time": "2026-04-05T18:00:00+08:00",
                    "actual_time": None,
                    "milestone_status": "delayed",
                    "is_overdue": True,
                },
            ],
            "logistics_status": None,
            "document_status": "not_required",
            "customs_status": None,
        },
        {
            "order_id": "ord_002",
            "order_no": "SO-2026-0002",
            "customer_id": "cus_002",
            "customer_name": "德国外贸客户B",
            "business_type": "外贸",
            "current_status": "待发货",
            "sub_status": "待单证",
            "risk_level": "high",
            "planned_delivery_date": "2026-04-08",
            "payment_status": "待回款",
            "currency": "USD",
            "total_amount": 48200.0,
            "milestones": [
                {
                    "milestone_type": "生产完成",
                    "planned_time": "2026-04-02T18:00:00+08:00",
                    "actual_time": "2026-04-02T16:00:00+08:00",
                    "milestone_status": "completed",
                    "is_overdue": False,
                }
            ],
            "logistics_status": "pending",
            "document_status": "missing",
            "customs_status": "pending",
        },
        {
            "order_id": "ord_003",
            "order_no": "SO-2026-0003",
            "customer_id": "cus_003",
            "customer_name": "美国渠道客户C",
            "business_type": "外贸",
            "current_status": "运输 / 交付中",
            "sub_status": "海运在途",
            "risk_level": "medium",
            "planned_delivery_date": "2026-04-18",
            "payment_status": "待回款",
            "currency": "USD",
            "total_amount": 76000.0,
            "milestones": [
                {
                    "milestone_type": "出运",
                    "planned_time": "2026-03-29T12:00:00+08:00",
                    "actual_time": "2026-03-30T08:00:00+08:00",
                    "milestone_status": "completed",
                    "is_overdue": True,
                }
            ],
            "logistics_status": "delayed",
            "document_status": "completed",
            "customs_status": "released",
        },
        {
            "order_id": "ord_004",
            "order_no": "SO-2026-0004",
            "customer_id": "cus_004",
            "customer_name": "华南电商客户D",
            "business_type": "内销",
            "current_status": "待回款",
            "sub_status": "客户已签收",
            "risk_level": "high",
            "planned_delivery_date": "2026-03-20",
            "payment_status": "逾期",
            "currency": "CNY",
            "total_amount": 56000.0,
            "milestones": [
                {
                    "milestone_type": "签收完成",
                    "planned_time": "2026-03-20T18:00:00+08:00",
                    "actual_time": "2026-03-20T16:30:00+08:00",
                    "milestone_status": "completed",
                    "is_overdue": False,
                }
            ],
            "logistics_status": "delivered",
            "document_status": "not_required",
            "customs_status": None,
        },
        {
            "order_id": "ord_005",
            "order_no": "SO-2026-0005",
            "customer_id": "cus_002",
            "customer_name": "德国外贸客户B",
            "business_type": "外贸",
            "current_status": "已确认",
            "sub_status": "待排产",
            "risk_level": "low",
            "planned_delivery_date": "2026-04-22",
            "payment_status": "未到期",
            "currency": "EUR",
            "total_amount": 32800.0,
            "milestones": [],
            "logistics_status": None,
            "document_status": "pending",
            "customs_status": None,
        },
    ]

    tasks = [
        {
            "task_id": "task_001",
            "task_type": "follow_up_agent",
            "task_title": "确认工厂恢复时间",
            "task_description": "生产里程碑延迟，需要跟进工厂反馈。",
            "related_order_id": "ord_001",
            "assignee_id": "user_sales_01",
            "priority": "high",
            "due_time": "2小时内",
            "task_status": "待处理",
            "created_at": "2026-04-01T09:00:00+08:00",
        },
        {
            "task_id": "task_002",
            "task_type": "customs_agent",
            "task_title": "补齐发货/报关单证",
            "task_description": "外贸订单待补齐 CI / PL / 报关委托书。",
            "related_order_id": "ord_002",
            "assignee_id": "user_sales_02",
            "priority": "high",
            "due_time": "4小时内",
            "task_status": "待处理",
            "created_at": "2026-04-01T10:00:00+08:00",
        },
    ]

    exceptions = [
        {
            "exception_id": "exception_001",
            "exception_type": "交付异常",
            "exception_level": "P2",
            "related_order_id": "ord_001",
            "source_event_id": "event_001",
            "owner_id": "user_sales_01",
            "suggestion": "联系工厂确认恢复时间并更新预计交付日期。",
            "exception_status": "已发现",
            "created_at": "2026-04-01T09:05:00+08:00",
        },
        {
            "exception_id": "exception_002",
            "exception_type": "回款异常",
            "exception_level": "P1",
            "related_order_id": "ord_004",
            "source_event_id": "event_003",
            "owner_id": "user_sales_01",
            "suggestion": "立即联系客户确认逾期回款原因。",
            "exception_status": "处理中",
            "created_at": "2026-04-01T09:20:00+08:00",
        },
    ]

    events = [
        {
            "event_id": "event_001",
            "event_type": "production.milestone_delayed",
            "event_time": "2026-04-01T08:58:00+08:00",
            "source_system": "kingdee_k3cloud",
            "biz_object_type": "order",
            "biz_object_id": "ord_001",
            "order_id": "ord_001",
            "customer_id": "cus_001",
            "priority": "P1",
            "payload": {"milestone_type": "生产完成", "delay_days": 2},
            "created_at": "2026-04-01T08:58:00+08:00",
        },
        {
            "event_id": "event_002",
            "event_type": "document.missing",
            "event_time": "2026-04-01T09:59:00+08:00",
            "source_system": "kingdee_k3cloud",
            "biz_object_type": "order",
            "biz_object_id": "ord_002",
            "order_id": "ord_002",
            "customer_id": "cus_002",
            "priority": "P1",
            "payload": {"missing_documents": ["CI", "PL", "报关委托书"]},
            "created_at": "2026-04-01T09:59:00+08:00",
        },
        {
            "event_id": "event_003",
            "event_type": "payment.overdue",
            "event_time": "2026-04-01T09:18:00+08:00",
            "source_system": "kingdee_k3cloud",
            "biz_object_type": "order",
            "biz_object_id": "ord_004",
            "order_id": "ord_004",
            "customer_id": "cus_004",
            "priority": "P1",
            "payload": {
                "receivable_amount": 56000.0,
                "received_amount": 0.0,
                "due_date": "2026-03-28",
                "overdue_days": 4,
            },
            "created_at": "2026-04-01T09:18:00+08:00",
        },
    ]

    agent_runs = [
        {
            "run_id": "agent_run_001",
            "agent_name": "Follow-up Agent",
            "trigger_event_type": "production.milestone_delayed",
            "order_id": "ord_001",
            "input_context": {"source": "seed"},
            "output_result": {"summary": "已识别生产延期风险。"},
            "created_at": "2026-04-01T09:01:00+08:00",
        },
        {
            "run_id": "agent_run_002",
            "agent_name": "Customs / Documentation Agent",
            "trigger_event_type": "document.missing",
            "order_id": "ord_002",
            "input_context": {"source": "seed"},
            "output_result": {"summary": "已识别单证缺失阻塞。"},
            "created_at": "2026-04-01T10:02:00+08:00",
        },
    ]

    notifications = [
        {
            "notification_id": "notification_001",
            "channel": "dingtalk",
            "template_code": "R002_follow_up_agent",
            "receiver_ids": ["user_sales_01"],
            "payload": {"message": "订单 SO-2026-0001 存在生产延期风险。"},
            "sent": True,
            "created_at": "2026-04-01T09:02:00+08:00",
        },
        {
            "notification_id": "notification_002",
            "channel": "dingtalk",
            "template_code": "R010_finance_agent",
            "receiver_ids": ["user_sales_01"],
            "payload": {"message": "订单 SO-2026-0004 已逾期，请尽快处理回款。"},
            "sent": True,
            "created_at": "2026-04-01T09:22:00+08:00",
        },
    ]

    return {
        "customers": customers,
        "orders": orders,
        "tasks": tasks,
        "exceptions": exceptions,
        "events": events,
        "agent_runs": agent_runs,
        "notifications": notifications,
    }


def build_seed_store(db_path: str | None = None) -> SQLiteStore:
    store = SQLiteStore(db_path or Path("data") / "atlas_trade_ai_demo.sqlite")
    store.seed(build_seed_payload())
    return store
