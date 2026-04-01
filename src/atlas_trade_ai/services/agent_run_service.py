from __future__ import annotations

from datetime import datetime

from atlas_trade_ai.core.store import SQLiteStore


class AgentRunService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def log_run(
        self,
        agent_name: str,
        trigger_event_type: str,
        order_id: str | None,
        input_context: dict,
        output_result: dict,
    ) -> dict:
        run_id = self.store.next_id("agent_run")
        item = {
            "run_id": run_id,
            "agent_name": agent_name,
            "trigger_event_type": trigger_event_type,
            "order_id": order_id,
            "input_context": input_context,
            "output_result": output_result,
            "created_at": datetime.now().astimezone().isoformat(),
        }
        return self.store.save_agent_run(item)

    def list_runs(self, agent_name: str | None = None) -> list[dict]:
        items = self.store.list_agent_runs()
        if agent_name:
            items = [item for item in items if item["agent_name"] == agent_name]
        return items
