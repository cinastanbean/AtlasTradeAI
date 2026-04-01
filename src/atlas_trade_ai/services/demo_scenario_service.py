from __future__ import annotations

from atlas_trade_ai.core.config_loader import JsonConfigLoader
from atlas_trade_ai.services.event_service import EventService


class DemoScenarioService:
    def __init__(self, loader: JsonConfigLoader, event_service: EventService) -> None:
        self.loader = loader
        self.event_service = event_service
        self._scenarios = loader.load("demo_scenarios.json")["scenarios"]

    def list_scenarios(self) -> list[dict]:
        return self._scenarios

    def run_scenario(self, code: str) -> dict:
        scenario = next(item for item in self._scenarios if item["code"] == code)
        result = self.event_service.write_event(scenario["event"])
        return {
            "scenario": {
                "code": scenario["code"],
                "name": scenario["name"],
                "description": scenario["description"],
            },
            "result": result,
        }
