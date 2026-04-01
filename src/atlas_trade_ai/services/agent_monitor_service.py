from __future__ import annotations

from atlas_trade_ai.core.store import SQLiteStore
from atlas_trade_ai.services.agent_registry_service import AgentRegistryService


class AgentMonitorService:
    def __init__(self, store: SQLiteStore, agent_registry_service: AgentRegistryService) -> None:
        self.store = store
        self.agent_registry_service = agent_registry_service

    def get_overview(self) -> dict:
        catalog = self.agent_registry_service.list_agents()
        runs = self.store.list_agent_runs()
        run_map: dict[str, list[dict]] = {}
        for item in runs:
            run_map.setdefault(item["agent_name"], []).append(item)

        agent_cards = []
        for item in catalog:
            agent_runs = run_map.get(item["name"], [])
            providers = {
                (run.get("output_result", {}).get("engine") or {}).get("provider", "unknown")
                for run in agent_runs[:20]
            }
            agent_cards.append(
                {
                    "agent_key": item["agent_key"],
                    "name": item["name"],
                    "layer": item["layer"],
                    "description": item["description"],
                    "execution_mode": item.get("execution_mode"),
                    "intelligence_type": item.get("intelligence_type"),
                    "subscribed_events": item.get("subscribed_events", []),
                    "run_count": len(agent_runs),
                    "last_run": agent_runs[0] if agent_runs else None,
                    "engine_providers": sorted(provider for provider in providers if provider),
                    "skills": self._build_skills(item),
                }
            )
        return {
            "agent_count": len(catalog),
            "active_agent_count": len([item for item in agent_cards if item["run_count"] > 0]),
            "agent_cards": agent_cards,
            "latest_runs": runs[:20],
        }

    def _build_skills(self, item: dict) -> list[str]:
        mapping = {
            "follow_up_agent": ["异常识别", "任务编排", "钉钉通知", "履约推进"],
            "sales_agent": ["商机推进", "报价转订单", "客户沟通建议"],
            "crm_agent": ["客户画像", "客户分层", "经营提醒"],
            "supply_chain_agent": ["排产建议", "供应链风险识别", "工厂协同"],
            "logistics_agent": ["交付时效判断", "物流协调", "ETA 同步"],
            "customs_agent": ["报关阻塞判断", "单证合规检查"],
            "finance_agent": ["回款风险识别", "催收建议", "账期跟进"],
            "customer_service_agent": ["投诉分流", "服务闭环", "售后沟通"],
            "document_intelligence_agent": ["单证抽取", "资料比对", "修正建议"],
            "operations_analyst_agent": ["经营复盘", "指标分析", "诊断摘要"],
            "knowledge_agent": ["案例归档", "SOP 沉淀", "知识复用"],
        }
        return mapping.get(item["agent_key"], ["通用处理"])
