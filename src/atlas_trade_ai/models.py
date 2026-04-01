from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TriggerEvent:
    event_id: str
    event_type: str
    event_time: str
    source_system: str
    biz_object_type: str
    biz_object_id: str


@dataclass(slots=True)
class OrderContext:
    order_id: str
    order_no: str
    current_status: str
    sub_status: str | None = None
    risk_level: str = "low"
    planned_delivery_date: str | None = None
    payment_status: str | None = None
    total_amount: float | None = None
    currency: str | None = None


@dataclass(slots=True)
class CustomerContext:
    customer_id: str
    customer_name: str
    customer_level: str = "普通客户"
    business_type: str = "外贸"
    owner_id: str | None = None


@dataclass(slots=True)
class Milestone:
    milestone_type: str
    planned_time: str | None = None
    actual_time: str | None = None
    milestone_status: str = "pending"
    is_overdue: bool = False


@dataclass(slots=True)
class ExceptionContext:
    exception_id: str
    exception_type: str
    exception_level: str
    exception_status: str


@dataclass(slots=True)
class FulfillmentContext:
    milestones: list[Milestone] = field(default_factory=list)
    latest_logistics_status: str | None = None
    document_status: str | None = None
    customs_status: str | None = None
    exceptions: list[ExceptionContext] = field(default_factory=list)


@dataclass(slots=True)
class PaymentContext:
    receivable_amount: float | None = None
    received_amount: float | None = None
    due_date: str | None = None
    overdue_days: int = 0


@dataclass(slots=True)
class AgentContext:
    trigger_event: TriggerEvent
    order: OrderContext
    customer: CustomerContext
    fulfillment: FulfillmentContext
    payment: PaymentContext

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AgentContext":
        fulfillment = payload.get("fulfillment_context", {})
        payment = payload.get("payment_context", {})

        milestones = [
            Milestone(**item) for item in fulfillment.get("milestones", [])
        ]
        exceptions = [
            ExceptionContext(
                exception_id=item.get("exception_id", "unknown_exception"),
                exception_type=item.get("exception_type", "未知异常"),
                exception_level=item.get("exception_level", "P3"),
                exception_status=item.get("exception_status", "已发现"),
            )
            for item in fulfillment.get("exceptions", [])
        ]

        return cls(
            trigger_event=TriggerEvent(**payload["trigger_event"]),
            order=OrderContext(**payload["order_context"]),
            customer=CustomerContext(**payload["customer_context"]),
            fulfillment=FulfillmentContext(
                milestones=milestones,
                latest_logistics_status=fulfillment.get("latest_logistics_status"),
                document_status=fulfillment.get("document_status"),
                customs_status=fulfillment.get("customs_status"),
                exceptions=exceptions,
            ),
            payment=PaymentContext(**payment),
        )


@dataclass(slots=True)
class RiskAssessment:
    level: str
    risk_type: str
    reason: str


@dataclass(slots=True)
class TaskDraft:
    title: str
    assignee_role: str
    priority: str
    due_hint: str


@dataclass(slots=True)
class ExceptionMark:
    exception_type: str
    exception_level: str
    reason: str


@dataclass(slots=True)
class AgentOutput:
    summary: str
    risk_assessment: RiskAssessment
    recommended_actions: list[str]
    task_drafts: list[TaskDraft]
    exception_marks: list[ExceptionMark]
    notification_draft: str
    engine: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "risk_assessment": {
                "level": self.risk_assessment.level,
                "risk_type": self.risk_assessment.risk_type,
                "reason": self.risk_assessment.reason,
            },
            "recommended_actions": self.recommended_actions,
            "task_drafts": [
                {
                    "title": item.title,
                    "assignee_role": item.assignee_role,
                    "priority": item.priority,
                    "due_hint": item.due_hint,
                }
                for item in self.task_drafts
            ],
            "exception_marks": [
                {
                    "exception_type": item.exception_type,
                    "exception_level": item.exception_level,
                    "reason": item.reason,
                }
                for item in self.exception_marks
            ],
            "notification_draft": self.notification_draft,
            "engine": self.engine,
        }
