from __future__ import annotations

from atlas_trade_ai.core.config_loader import JsonConfigLoader
from atlas_trade_ai.services.agent_run_service import AgentRunService
from atlas_trade_ai.services.agent_service import FollowUpAgentService
from atlas_trade_ai.services.intelligent_role_agent_service import IntelligentRoleAgentService


class AgentRegistryService:
    def __init__(self, loader: JsonConfigLoader, agent_run_service: AgentRunService) -> None:
        self.loader = loader
        self.agent_run_service = agent_run_service
        self._catalog = self.loader.load("agent_catalog.json")["agents"]
        self._services = self._build_services()

    def _build_services(self) -> dict[str, object]:
        services: dict[str, object] = {
            "follow_up_agent": FollowUpAgentService(self.agent_run_service)
        }
        for item in self._catalog:
            key = item["agent_key"]
            if key == "follow_up_agent":
                continue
            services[key] = IntelligentRoleAgentService(
                agent_key=key,
                agent_name=item["name"],
                agent_run_service=self.agent_run_service,
                execution_mode=item.get("execution_mode", "hybrid"),
                intelligence_type=item.get("intelligence_type"),
            )
        return services

    def list_agents(self) -> list[dict]:
        return self._catalog

    def get_agent_service(self, agent_key: str) -> object | None:
        return self._services.get(agent_key)
