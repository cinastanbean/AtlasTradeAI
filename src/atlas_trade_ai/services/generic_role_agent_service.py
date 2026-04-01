from __future__ import annotations

from atlas_trade_ai.services.agent_run_service import AgentRunService


class GenericRoleAgentService:
    def __init__(
        self,
        agent_key: str,
        agent_name: str,
        agent_run_service: AgentRunService,
    ) -> None:
        self.agent_key = agent_key
        self.agent_name = agent_name
        self.agent_run_service = agent_run_service

    def run(self, payload: dict) -> dict:
        event_type = payload["trigger_event"]["event_type"]
        order = payload["order_context"]
        customer = payload["customer_context"]
        summary = self._build_summary(event_type, order, customer)
        result = {
            "summary": summary,
            "risk_assessment": self._build_risk(event_type),
            "recommended_actions": self._build_actions(event_type),
            "task_drafts": self._build_tasks(event_type),
            "exception_marks": self._build_exceptions(event_type),
            "notification_draft": f"{self.agent_name} 已接管事件 {event_type}，订单 {order['order_no']} 需要继续处理。",
        }
        self.agent_run_service.log_run(
            agent_name=self.agent_name,
            trigger_event_type=event_type,
            order_id=order["order_id"],
            input_context=payload,
            output_result=result,
        )
        return result

    def _build_summary(self, event_type: str, order: dict, customer: dict) -> str:
        return (
            f"{self.agent_name} 已收到事件 {event_type}，"
            f"当前订单 {order['order_no']} 属于客户 {customer['customer_name']}，"
            "系统已生成对应的执行建议。"
        )

    def _build_risk(self, event_type: str) -> dict:
        mapping = {
            "supply_chain_agent": ("medium", "supply_chain_risk"),
            "logistics_agent": ("medium", "logistics_risk"),
            "customs_agent": ("high", "compliance_risk"),
            "finance_agent": ("high", "finance_risk"),
            "sales_agent": ("low", "sales_followup"),
            "crm_agent": ("low", "customer_management"),
            "customer_service_agent": ("medium", "after_sales_risk"),
        }
        level, risk_type = mapping.get(self.agent_key, ("low", "generic"))
        return {
            "level": level,
            "risk_type": risk_type,
            "reason": f"{self.agent_name} 基于事件 {event_type} 进行了角色分析。",
        }

    def _build_actions(self, event_type: str) -> list[str]:
        action_map = {
            "supply_chain_agent": [
                "确认工厂与供应商的最新执行计划",
                "评估订单是否需要调整排产或采购优先级",
            ],
            "logistics_agent": [
                "确认当前发运条件和物流节点状态",
                "评估是否需要同步客户新的到货时间",
            ],
            "customs_agent": [
                "检查单证完整性和报关资料一致性",
                "确认是否存在阻塞发货的合规问题",
            ],
            "finance_agent": [
                "确认账期、应收和付款承诺",
                "评估是否需要升级为资金风险订单",
            ],
            "sales_agent": [
                "更新销售跟进动作",
                "确认客户沟通口径和下一步商机动作",
            ],
            "crm_agent": [
                "更新客户画像和客户等级判断",
                "补充客户经营备注与提醒",
            ],
            "customer_service_agent": [
                "确认客户问题闭环路径",
                "沉淀售后处理结果与客户反馈",
            ],
        }
        return action_map.get(self.agent_key, [f"{self.agent_name} 处理中：{event_type}"])

    def _build_tasks(self, event_type: str) -> list[dict]:
        title_map = {
            "supply_chain_agent": "确认供应链执行计划",
            "logistics_agent": "确认物流执行状态",
            "customs_agent": "检查单证与报关资料",
            "finance_agent": "跟进财务风险处理",
            "sales_agent": "更新销售跟进行动",
            "crm_agent": "更新客户经营状态",
            "customer_service_agent": "跟进售后处理进展",
        }
        return [
            {
                "title": title_map.get(self.agent_key, f"{self.agent_name} 任务"),
                "assignee_role": self.agent_name,
                "priority": "medium",
                "due_hint": "今天内",
            }
        ]

    def _build_exceptions(self, event_type: str) -> list[dict]:
        if self.agent_key == "finance_agent" and event_type == "payment.overdue":
            return [
                {
                    "exception_type": "回款异常",
                    "exception_level": "P1",
                    "reason": "Finance Agent 识别到逾期回款风险。",
                }
            ]
        if self.agent_key == "customs_agent" and event_type == "document.missing":
            return [
                {
                    "exception_type": "单证异常",
                    "exception_level": "P1",
                    "reason": "Customs Agent 识别到单证缺失风险。",
                }
            ]
        if self.agent_key == "logistics_agent" and event_type == "logistics.delayed":
            return [
                {
                    "exception_type": "物流异常",
                    "exception_level": "P2",
                    "reason": "Logistics Agent 识别到运输延误。",
                }
            ]
        return []
