from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AgentRunRead(BaseModel):
    run_id: str
    agent_name: str
    trigger_event_type: str
    order_id: str | None = None
    input_context: dict[str, Any]
    output_result: dict[str, Any]
