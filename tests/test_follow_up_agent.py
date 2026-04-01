from atlas_trade_ai.agent import FollowUpAgent
from atlas_trade_ai.models import AgentContext


def _build_context(event_type: str, overdue_days: int = 0) -> AgentContext:
    return AgentContext.from_dict(
        {
            "trigger_event": {
                "event_id": "evt_test",
                "event_type": event_type,
                "event_time": "2026-04-01T10:30:00+08:00",
                "source_system": "erp",
                "biz_object_type": "order",
                "biz_object_id": "ord_test",
            },
            "order_context": {
                "order_id": "ord_test",
                "order_no": "SO-TEST-001",
                "current_status": "执行中",
                "sub_status": "生产中",
                "risk_level": "medium",
                "planned_delivery_date": "2026-04-10",
                "payment_status": "待回款",
            },
            "customer_context": {
                "customer_id": "cus_test",
                "customer_name": "测试客户",
                "customer_level": "重点客户",
                "business_type": "外贸",
                "owner_id": "owner_1",
            },
            "fulfillment_context": {
                "milestones": [],
                "latest_logistics_status": None,
                "document_status": "pending",
                "customs_status": None,
                "exceptions": [],
            },
            "payment_context": {
                "receivable_amount": 100.0,
                "received_amount": 0.0,
                "due_date": "2026-04-15",
                "overdue_days": overdue_days,
            },
        }
    )


def test_production_delay_generates_delivery_risk() -> None:
    result = FollowUpAgent().run(_build_context("production.milestone_delayed"))
    assert result.risk_assessment.risk_type == "delivery_delay"
    assert result.task_drafts
    assert result.exception_marks


def test_payment_overdue_generates_exception_mark() -> None:
    result = FollowUpAgent().run(_build_context("payment.overdue", overdue_days=7))
    assert result.risk_assessment.risk_type == "payment_overdue"
    assert result.exception_marks[0].exception_type == "回款异常"


def test_generic_event_still_creates_followup_task() -> None:
    result = FollowUpAgent().run(_build_context("order.status_changed"))
    assert result.risk_assessment.risk_type == "followup_required"
    assert result.task_drafts[0].title == "复核订单状态变化"


def test_hybrid_agent_without_api_key_falls_back_to_rules() -> None:
    result = FollowUpAgent().run(_build_context("document.missing"))
    assert result.engine["llm_used"] is False
    assert result.engine["provider"] == "rule-engine"
