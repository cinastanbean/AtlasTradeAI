from __future__ import annotations

from typing import Any

from atlas_trade_ai.llm import create_enhancer, get_provider_name
from atlas_trade_ai.services.agent_run_service import AgentRunService


class IntelligentRoleAgentService:
    def __init__(
        self,
        agent_key: str,
        agent_name: str,
        agent_run_service: AgentRunService,
        execution_mode: str = "hybrid",
        intelligence_type: str | None = None,
    ) -> None:
        self.agent_key = agent_key
        self.agent_name = agent_name
        self.agent_run_service = agent_run_service
        self.execution_mode = execution_mode
        self.intelligence_type = intelligence_type or "业务判断"
        self.enhancer = create_enhancer()

    def run(self, payload: dict) -> dict:
        event_type = payload["trigger_event"]["event_type"]
        order = payload["order_context"]
        customer = payload["customer_context"]
        payment = payload.get("payment_context", {})
        raw = self._build_rule_result(event_type, order, customer, payment, payload)
        result = self._maybe_enhance(raw, event_type, order, customer)
        self.agent_run_service.log_run(
            agent_name=self.agent_name,
            trigger_event_type=event_type,
            order_id=order["order_id"],
            input_context=payload,
            output_result=result,
        )
        return result

    def _build_rule_result(
        self,
        event_type: str,
        order: dict,
        customer: dict,
        payment: dict,
        payload: dict,
    ) -> dict:
        event_payload = payload.get("event_payload") or payload.get("trigger_event", {}).get("payload", {})
        builder = {
            "sales_agent": self._build_sales_result,
            "crm_agent": self._build_crm_result,
            "supply_chain_agent": self._build_supply_chain_result,
            "logistics_agent": self._build_logistics_result,
            "customs_agent": self._build_customs_result,
            "finance_agent": self._build_finance_result,
            "customer_service_agent": self._build_customer_service_result,
            "document_intelligence_agent": self._build_document_intelligence_result,
            "operations_analyst_agent": self._build_operations_analyst_result,
            "knowledge_agent": self._build_knowledge_result,
        }.get(self.agent_key, self._build_fallback_result)
        result = builder(event_type, order, customer, payment, payload | {"event_payload": event_payload})
        result["engine"] = {
            "mode": self.execution_mode,
            "provider": "rule-engine",
            "llm_used": False,
            "intelligence_type": self.intelligence_type,
        }
        return result

    def _maybe_enhance(
        self,
        result: dict,
        event_type: str,
        order: dict,
        customer: dict,
    ) -> dict:
        provider_name = get_provider_name(self.enhancer)
        
        if self.execution_mode != "hybrid":
            return result
        if not self.enhancer.is_enabled():
            result["engine"]["fallback_reason"] = f"{provider_name.upper()}_API_KEY 未配置"
            return result

        prompt = f"""
你是贸易公司的 {self.agent_name}，请在不改变风险等级、任务结构和异常结构的前提下，
优化以下输出的中文表达，使其更适合作为业务系统的摘要、建议和钉钉通知。

Agent: {self.agent_name}
能力: {self.intelligence_type}
事件: {event_type}
订单: {order['order_no']} / {order.get('current_status')}
客户: {customer['customer_name']}
当前摘要: {result['summary']}
当前建议: {result['recommended_actions']}
当前通知: {result['notification_draft']}

只返回 JSON:
{{
  "summary": "string",
  "recommended_actions": ["string", "string", "string"],
  "notification_draft": "string"
}}
"""
        enhanced = self.enhancer.enhance(prompt)
        if not enhanced:
            result["engine"]["fallback_reason"] = "LLM 调用失败，已回退规则结果"
            return result

        result["summary"] = enhanced.get("summary") or result["summary"]
        result["recommended_actions"] = enhanced.get("recommended_actions") or result["recommended_actions"]
        result["notification_draft"] = enhanced.get("notification_draft") or result["notification_draft"]
        result["engine"] = {
            "mode": "hybrid",
            "provider": provider_name,
            "llm_used": True,
            "model": self.enhancer.model,
            "intelligence_type": self.intelligence_type,
        }
        return result

    def _base_result(
        self,
        summary: str,
        risk_level: str,
        risk_type: str,
        reason: str,
        actions: list[str],
        tasks: list[dict],
        exceptions: list[dict],
        notification: str,
    ) -> dict:
        return {
            "summary": summary,
            "risk_assessment": {
                "level": risk_level,
                "risk_type": risk_type,
                "reason": reason,
            },
            "recommended_actions": actions,
            "task_drafts": tasks,
            "exception_marks": exceptions,
            "notification_draft": notification,
        }

    def _build_sales_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        accepted_amount = payload.get("event_payload", {}).get("accepted_amount") or payment.get("receivable_amount")
        reason = "客户已接受报价，商机进入订单确认与成交推进阶段。"
        return self._base_result(
            summary=f"Sales Agent 识别到客户 {customer['customer_name']} 已接受报价，订单 {order['order_no']} 需要尽快推进成交确认。",
            risk_level="low",
            risk_type="sales_conversion",
            reason=reason,
            actions=[
                "确认最终规格、数量与交付条件是否锁定",
                "推动销售订单或 PI 尽快确认并同步客户",
                "将成交信息反馈给 CRM 和订单中枢",
            ],
            tasks=[
                {"title": "确认成交条件并转订单", "assignee_role": "销售", "priority": "medium", "due_hint": "今天内"},
                {"title": "复核成交金额与规格", "assignee_role": "销售", "priority": "medium", "due_hint": "今天内"},
            ],
            exceptions=[],
            notification=f"报价已被客户接受，订单 {order['order_no']} 进入成交推进阶段，金额 {accepted_amount or '-'}。",
        )

    def _build_crm_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = "客户发生关键经营事件，需要更新画像、分层和后续提醒。"
        high_value = customer.get("customer_level") in {"战略客户", "重点客户"}
        return self._base_result(
            summary=f"CRM Agent 已识别客户 {customer['customer_name']} 的经营状态变化，建议更新客户画像与后续跟进策略。",
            risk_level="low" if high_value else "medium",
            risk_type="customer_management",
            reason=reason,
            actions=[
                "更新客户画像、成交阶段与关键偏好信息",
                "根据事件结果调整客户分层和提醒策略",
                "补充可复用的客户经营备注供销售与客服参考",
            ],
            tasks=[
                {"title": "更新客户画像与经营标签", "assignee_role": "CRM", "priority": "medium", "due_hint": "今天内"},
            ],
            exceptions=[],
            notification=f"CRM Agent 已记录客户 {customer['customer_name']} 的关键经营变化，建议同步画像和分层。",
        )

    def _build_supply_chain_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = "供应链执行进度与计划存在偏差，需要重新确认产能、物料和排期。"
        return self._base_result(
            summary=f"Supply Chain Agent 识别到订单 {order['order_no']} 的执行计划存在波动，需要尽快重排产并校验供应条件。",
            risk_level="high" if event_type == "production.milestone_delayed" else "medium",
            risk_type="supply_chain_risk",
            reason=reason,
            actions=[
                "确认工厂产能与物料齐套状态",
                "必要时调整排产顺序或切换备选供应商",
                "将最新预计完成时间回写订单中枢",
            ],
            tasks=[
                {"title": "重检排产与物料条件", "assignee_role": "供应链", "priority": "high", "due_hint": "2小时内"},
            ],
            exceptions=[
                {
                    "exception_type": "供应链异常",
                    "exception_level": "P1" if event_type == "production.milestone_delayed" else "P2",
                    "reason": reason,
                }
            ] if event_type == "production.milestone_delayed" else [],
            notification=f"供应链执行出现偏差，订单 {order['order_no']} 需要重新确认排产与物料。",
        )

    def _build_logistics_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = "物流节点与客户承诺时效之间存在偏差，需要尽快确认最新交付计划。"
        return self._base_result(
            summary=f"Logistics Agent 正在评估订单 {order['order_no']} 的交付链路，建议同步最新发运与到货时效。",
            risk_level="medium",
            risk_type="logistics_risk",
            reason=reason,
            actions=[
                "确认承运商当前节点和预计到达时间",
                "判断是否需要变更运输方案或提前通知客户",
                "将物流状态回写至订单看板",
            ],
            tasks=[
                {"title": "确认物流节点与 ETA", "assignee_role": "物流", "priority": "medium", "due_hint": "今天内"},
            ],
            exceptions=[
                {
                    "exception_type": "物流异常",
                    "exception_level": "P2",
                    "reason": "物流时效偏离承诺节点。",
                }
            ] if event_type == "logistics.delayed" else [],
            notification=f"订单 {order['order_no']} 的物流计划需要更新，请确认最新 ETA 并准备客户同步。",
        )

    def _build_customs_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = "单证完整性或清关合规条件不足，可能直接阻塞发货或清关。"
        return self._base_result(
            summary=f"Customs / Documentation Agent 发现订单 {order['order_no']} 存在单证或清关阻塞风险。",
            risk_level="high",
            risk_type="compliance_risk",
            reason=reason,
            actions=[
                "核对 CI、PL、报关委托书及客户要求资料是否齐全",
                "检查报关要素、品名、数量和申报信息是否一致",
                "若已临近截关时间，立即升级为阻塞异常",
            ],
            tasks=[
                {"title": "复核单证一致性并补齐缺失资料", "assignee_role": "单证", "priority": "high", "due_hint": "4小时内"},
            ],
            exceptions=[
                {
                    "exception_type": "单证异常",
                    "exception_level": "P1",
                    "reason": reason,
                }
            ],
            notification=f"订单 {order['order_no']} 存在单证/清关阻塞风险，请立即处理。",
        )

    def _build_finance_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        overdue_days = payment.get("overdue_days", 0)
        reason = (
            f"客户回款已逾期 {overdue_days} 天，资金回收风险正在上升。"
            if event_type == "payment.overdue"
            else "订单回款已接近账期，需要提前做好催收和到账确认。"
        )
        return self._base_result(
            summary=f"Finance Agent 已对订单 {order['order_no']} 的回款状态完成识别，建议立即推进账期确认与催收动作。",
            risk_level="high" if event_type == "payment.overdue" else "medium",
            risk_type="finance_risk",
            reason=reason,
            actions=[
                "确认客户付款计划与到账承诺",
                "同步销售负责人评估客户关系与沟通口径",
                "根据金额与逾期天数判断是否升级风险等级",
            ],
            tasks=[
                {"title": "跟进客户回款承诺", "assignee_role": "财务", "priority": "high" if event_type == "payment.overdue" else "medium", "due_hint": "今天内"},
            ],
            exceptions=[
                {
                    "exception_type": "回款异常",
                    "exception_level": "P1",
                    "reason": reason,
                }
            ] if event_type == "payment.overdue" else [],
            notification=f"订单 {order['order_no']} 存在回款风险，请财务与销售协同推进。",
        )

    def _build_customer_service_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        complaint = payload.get("event_payload", {}).get("complaint_type", "售后问题")
        reason = "客户已发起售后投诉，需要快速分流、响应和闭环。"
        return self._base_result(
            summary=f"Customer Service Agent 已识别到订单 {order['order_no']} 的售后问题“{complaint}”，建议立即进入客服处理流程。",
            risk_level="high" if event_type == "after_sales.complaint_created" else "medium",
            risk_type="after_sales_risk",
            reason=reason,
            actions=[
                "确认问题责任归属、客户诉求和处理时限",
                "同步销售与履约侧准备统一对外口径",
                "记录处理结果并形成可复用的售后知识",
            ],
            tasks=[
                {"title": "建立售后问题处理单", "assignee_role": "客服", "priority": "high", "due_hint": "2小时内"},
            ],
            exceptions=[
                {
                    "exception_type": "售后异常",
                    "exception_level": "P1",
                    "reason": reason,
                }
            ] if event_type == "after_sales.complaint_created" else [],
            notification=f"订单 {order['order_no']} 出现售后投诉，请客服尽快介入并同步处理进度。",
        )

    def _build_fallback_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = f"{self.agent_name} 已收到事件 {event_type}，当前采用通用角色处理模板。"
        return self._base_result(
            summary=reason,
            risk_level="low",
            risk_type="generic_role_processing",
            reason=reason,
            actions=["复核当前业务上下文并生成下一步动作"],
            tasks=[{"title": f"{self.agent_name} 跟进任务", "assignee_role": self.agent_name, "priority": "medium", "due_hint": "今天内"}],
            exceptions=[],
            notification=f"{self.agent_name} 已接管事件 {event_type}。",
        )

    def _build_document_intelligence_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = "单证资料需要进一步抽取、比对和一致性校验，以减少人工检查成本。"
        return self._base_result(
            summary=f"Document Intelligence Agent 已对订单 {order['order_no']} 的单证问题进行语义分析，建议优先检查一致性和缺失项。",
            risk_level="high",
            risk_type="document_intelligence",
            reason=reason,
            actions=[
                "抽取事件中的缺失资料与驳回原因",
                "比对 CI、PL、报关资料中的品名、数量、材质和申报要素",
                "输出修正清单并给单证人员参考",
            ],
            tasks=[
                {"title": "生成单证修正清单", "assignee_role": "单证", "priority": "high", "due_hint": "2小时内"},
            ],
            exceptions=[],
            notification=f"Document Intelligence Agent 已生成订单 {order['order_no']} 的单证检查建议。",
        )

    def _build_operations_analyst_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = "当前事件可用于经营复盘、异常归因和经营指标分析。"
        return self._base_result(
            summary=f"Operations Analyst Agent 已识别订单 {order['order_no']} 的经营分析价值，建议纳入日报和复盘结论。",
            risk_level="low" if event_type == "payment.completed" else "medium",
            risk_type="operations_analysis",
            reason=reason,
            actions=[
                "沉淀本次事件对交付、回款或服务的影响",
                "判断是否需要进入经营日报、周报或专项复盘",
                "提炼异常归因与改进建议供管理层参考",
            ],
            tasks=[
                {"title": "生成经营分析摘要", "assignee_role": "运营分析", "priority": "medium", "due_hint": "今天内"},
            ],
            exceptions=[],
            notification=f"Operations Analyst Agent 已为订单 {order['order_no']} 生成经营复盘建议。",
        )

    def _build_knowledge_result(self, event_type: str, order: dict, customer: dict, payment: dict, payload: dict) -> dict:
        reason = "当前事件具有知识沉淀价值，适合提炼为 SOP、案例或经验库条目。"
        return self._base_result(
            summary=f"Knowledge Agent 已判断订单 {order['order_no']} 的本次事件可沉淀为知识资产，建议归档处理经验。",
            risk_level="low",
            risk_type="knowledge_capture",
            reason=reason,
            actions=[
                "提取本次事件中的关键处理动作和经验",
                "归档为案例、SOP 补充项或 FAQ",
                "为后续 Agent 提供可复用知识线索",
            ],
            tasks=[
                {"title": "归档案例与经验", "assignee_role": "知识管理", "priority": "low", "due_hint": "本周内"},
            ],
            exceptions=[],
            notification=f"Knowledge Agent 已为订单 {order['order_no']} 生成知识归档建议。",
        )
