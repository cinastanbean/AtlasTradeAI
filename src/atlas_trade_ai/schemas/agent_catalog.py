from __future__ import annotations

from pydantic import BaseModel


class AgentCatalogRead(BaseModel):
    agent_key: str
    name: str
    layer: str
    description: str
    subscribed_events: list[str]
    execution_mode: str | None = None
    intelligence_type: str | None = None
