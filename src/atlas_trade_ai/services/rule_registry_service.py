from __future__ import annotations

from atlas_trade_ai.core.config_loader import JsonConfigLoader


class RuleRegistryService:
    def __init__(self, loader: JsonConfigLoader) -> None:
        self.loader = loader
        self._event_catalog = loader.load("event_catalog.json")
        self._workflow_rules = loader.load("workflow_rules.json")

    def list_events(self) -> list[dict]:
        return self._event_catalog["events"]

    def list_rules(self) -> list[dict]:
        return self._workflow_rules["rules"]

    def get_rule_for_event(self, event_type: str) -> dict | None:
        for rule in self._workflow_rules["rules"]:
            if rule["event_type"] == event_type:
                if "subscribers" not in rule and "subscriber" in rule:
                    rule = rule | {"subscribers": [rule["subscriber"]]}
                return rule
        return None
