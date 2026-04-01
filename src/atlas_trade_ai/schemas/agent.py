from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class FollowUpAgentRunRequest(BaseModel):
    trigger_event: dict[str, Any]
    order_context: dict[str, Any]
    customer_context: dict[str, Any]
    fulfillment_context: dict[str, Any]
    payment_context: dict[str, Any]


class FollowUpAgentRunResponse(BaseModel):
    summary: str
    risk_assessment: dict[str, Any]
    recommended_actions: list[str]
    task_drafts: list[dict[str, Any]]
    exception_marks: list[dict[str, Any]]
    notification_draft: str
    engine: dict[str, Any] | None = None
