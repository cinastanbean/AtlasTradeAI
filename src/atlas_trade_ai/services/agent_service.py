from __future__ import annotations

from atlas_trade_ai.agent import FollowUpAgent
from atlas_trade_ai.models import AgentContext


class FollowUpAgentService:
    def __init__(self) -> None:
        self.agent = FollowUpAgent()

    def run(self, payload: dict) -> dict:
        context = AgentContext.from_dict(payload)
        return self.agent.run(context).to_dict()
