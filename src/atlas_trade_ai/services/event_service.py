from __future__ import annotations

from atlas_trade_ai.core.store import InMemoryStore
from atlas_trade_ai.services.workflow_service import WorkflowService


class EventService:
    def __init__(
        self,
        store: InMemoryStore,
        workflow_service: WorkflowService,
    ) -> None:
        self.store = store
        self.workflow_service = workflow_service

    def write_event(self, payload: dict) -> dict:
        event_id = payload.get("event_id") or self.store.next_id("event")
        item = payload | {"event_id": event_id}
        self.store.events[event_id] = item
        workflow_result = self.workflow_service.process_event(item)

        return {
            "event_id": event_id,
            "accepted": True,
            "matched_rule": workflow_result["matched_rule"],
            "generated_task_ids": workflow_result["generated_task_ids"],
            "generated_exception_ids": workflow_result["generated_exception_ids"],
            "notification_ids": workflow_result["notification_ids"],
        }

    def list_events(self, order_id: str | None = None) -> list[dict]:
        items = list(self.store.events.values())
        if order_id:
            items = [item for item in items if item.get("order_id") == order_id]
        return items
