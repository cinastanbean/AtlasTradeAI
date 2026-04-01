from __future__ import annotations

from .models import AgentContext, AgentOutput
from .rules import build_output, evaluate_context


class FollowUpAgent:
    """Rule-based prototype for the first follow-up agent version."""

    def run(self, context: AgentContext) -> AgentOutput:
        decision = evaluate_context(context)
        return build_output(context, decision)
