from __future__ import annotations

import os

from .llm import create_enhancer, get_provider_name
from .models import AgentContext, AgentOutput
from .rules import build_output, evaluate_context


class FollowUpAgent:
    """Hybrid follow-up agent with rules as the stable execution backbone."""

    def __init__(self) -> None:
        self.enhancer = create_enhancer()
        self.mode = os.getenv("ATLAS_AGENT_MODE", "hybrid")

    def run(self, context: AgentContext) -> AgentOutput:
        decision = evaluate_context(context)
        output = build_output(context, decision)
        enhanced = self._enhance_with_llm(context, output)
        return enhanced or output

    def _enhance_with_llm(
        self,
        context: AgentContext,
        output: AgentOutput,
    ) -> AgentOutput | None:
        provider_name = get_provider_name(self.enhancer)
        
        if self.mode == "rules":
            output.engine = {"mode": "rules", "provider": "rule-engine", "llm_used": False}
            return output
        if not self.enhancer.is_enabled():
            output.engine = {
                "mode": "hybrid",
                "provider": "rule-engine",
                "llm_used": False,
                "fallback_reason": f"{provider_name.upper()}_API_KEY 未配置",
            }
            return output

        prompt = self._build_prompt(context, output)
        enhanced = self.enhancer.enhance(prompt)
        if not enhanced:
            output.engine = {
                "mode": "hybrid",
                "provider": "rule-engine",
                "llm_used": False,
                "fallback_reason": "LLM 调用失败，已回退规则结果",
            }
            return output

        summary = enhanced.get("summary") or output.summary
        recommended_actions = enhanced.get("recommended_actions") or output.recommended_actions
        notification_draft = enhanced.get("notification_draft") or output.notification_draft
        output.summary = summary
        output.recommended_actions = recommended_actions[:5]
        output.notification_draft = notification_draft
        output.engine = {
            "mode": "hybrid",
            "provider": provider_name,
            "llm_used": True,
            "model": self.enhancer.model,
        }
        return output

    def _build_prompt(self, context: AgentContext, output: AgentOutput) -> str:
        return f"""
你是贸易公司的资深跟单经理，请在不改变风险判断和任务结构的前提下，
优化以下输出的中文表达，让摘要、建议和通知更适合业务看板和钉钉通知。

订单号: {context.order.order_no}
客户: {context.customer.customer_name}
事件: {context.trigger_event.event_type}
当前状态: {context.order.current_status}/{context.order.sub_status}
规则摘要: {output.summary}
规则建议: {output.recommended_actions}
规则通知: {output.notification_draft}

请只返回 JSON，对应字段：
{{
  "summary": "string",
  "recommended_actions": ["string", "string", "string"],
  "notification_draft": "string"
}}
"""
