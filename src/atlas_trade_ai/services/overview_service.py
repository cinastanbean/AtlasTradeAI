from __future__ import annotations


class OverviewService:
    def get_architecture(self) -> dict:
        return {
            "hub": {
                "name": "订单中枢",
                "type": "hub",
                "description": "负责订单主视图、状态机、里程碑和事件分发",
            },
            "layers": [
                {
                    "name": "客户经营层",
                    "type": "layer",
                    "description": "承接客户开发、报价与 CRM 沉淀",
                },
                {
                    "name": "履约推进层",
                    "type": "layer",
                    "description": "承接跟单、任务、异常和催办动作",
                },
                {
                    "name": "供应链执行层",
                    "type": "layer",
                    "description": "承接工厂、采购、排产和供应协同",
                },
                {
                    "name": "交付与合规层",
                    "type": "layer",
                    "description": "承接物流、单证和报关流程",
                },
                {
                    "name": "资金结算层",
                    "type": "layer",
                    "description": "承接回款、利润和结算管理",
                },
                {
                    "name": "售后服务层",
                    "type": "layer",
                    "description": "承接投诉、售后和客户维护闭环",
                },
            ],
            "modules": [
                "客户中心",
                "订单中心",
                "任务中心",
                "异常中心",
                "事件中心",
                "回款中心",
            ],
            "agents": [
                "Sales Agent",
                "CRM Agent",
                "Follow-up Agent",
                "Supply Chain Agent",
                "Logistics Agent",
                "Customs / Documentation Agent",
                "Finance Agent",
                "Customer Service Agent",
            ],
        }
