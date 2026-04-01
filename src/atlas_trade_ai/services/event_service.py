from __future__ import annotations

from datetime import datetime

from atlas_trade_ai.core.store import SQLiteStore
from atlas_trade_ai.services.workflow_service import WorkflowService


class EventService:
    def __init__(
        self,
        store: SQLiteStore,
        workflow_service: WorkflowService,
    ) -> None:
        self.store = store
        self.workflow_service = workflow_service

    def write_event(self, payload: dict) -> dict:
        event_id = payload.get("event_id") or self.store.next_id("event")
        item = payload | {
            "event_id": event_id,
            "created_at": payload.get("created_at") or datetime.now().astimezone().isoformat(),
        }
        self.store.save_event(item)
        workflow_result = self.workflow_service.process_event(item)

        return {
            "event_id": event_id,
            "accepted": True,
            "matched_rule": workflow_result["matched_rule"],
            "orchestration": workflow_result.get("orchestration"),
            "generated_task_ids": workflow_result["generated_task_ids"],
            "generated_exception_ids": workflow_result["generated_exception_ids"],
            "notification_ids": workflow_result["notification_ids"],
        }

    def list_events(self, order_id: str | None = None) -> list[dict]:
        items = self.store.list_events()
        if order_id:
            items = [item for item in items if item.get("order_id") == order_id]
        return items
