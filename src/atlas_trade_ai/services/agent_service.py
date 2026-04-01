from __future__ import annotations

from atlas_trade_ai.agent import FollowUpAgent
from atlas_trade_ai.models import AgentContext
from atlas_trade_ai.services.agent_run_service import AgentRunService


class FollowUpAgentService:
    def __init__(self, agent_run_service: AgentRunService | None = None) -> None:
        self.agent = FollowUpAgent()
        self.agent_run_service = agent_run_service

    def run(self, payload: dict) -> dict:
        context = AgentContext.from_dict(payload)
        result = self.agent.run(context).to_dict()
        if self.agent_run_service is not None:
            self.agent_run_service.log_run(
                agent_name="Follow-up Agent",
                trigger_event_type=context.trigger_event.event_type,
                order_id=context.order.order_id,
                input_context=payload,
                output_result=result,
            )
        return result
