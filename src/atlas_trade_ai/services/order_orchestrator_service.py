from __future__ import annotations

from atlas_trade_ai.core.config_loader import JsonConfigLoader
from atlas_trade_ai.core.store import SQLiteStore
from atlas_trade_ai.services.agent_run_service import AgentRunService
from atlas_trade_ai.services.order_service import OrderService


class OrderOrchestratorService:
    def __init__(
        self,
        store: SQLiteStore,
        order_service: OrderService,
        agent_run_service: AgentRunService,
        loader: JsonConfigLoader,
    ) -> None:
        self.store = store
        self.order_service = order_service
        self.agent_run_service = agent_run_service
        config = loader.load("order_orchestration_rules.json")
        self.status_layers = config["status_layers"]
        self.rules = {item["event_type"]: item for item in config["rules"]}

    def orchestrate(self, payload: dict, subscribers: list[str]) -> dict:
        order_id = payload.get("order_id")
        if not order_id:
            return {
                "applied": False,
                "status_changed": False,
                "blocked": False,
                "decision_summary": "事件未绑定订单，未触发订单中枢编排。",
                "next_agents": subscribers,
            }

        order = self.order_service.get_order(order_id)
        previous_status = order.get("current_status")
        previous_sub_status = order.get("sub_status")
        rule = self.rules.get(payload["event_type"])
        if rule is None:
            current_layer = self._layer_for_status(previous_status)
            result = {
                "applied": False,
                "status_changed": False,
                "status_before": previous_status,
                "status_after": previous_status,
                "sub_status_before": previous_sub_status,
                "sub_status_after": previous_sub_status,
                "current_layer": current_layer,
                "target_layer": current_layer,
                "blocked": False,
                "next_owner_agent": subscribers[0] if subscribers else None,
                "next_agents": subscribers,
                "decision_summary": "当前事件未命中订单编排规则，保持现有阶段。",
            }
            self._log_run(order_id, payload["event_type"], payload, result)
            return result

        status_after = rule["status_after"]
        sub_status_after = rule["sub_status"]
        current_layer = self._layer_for_status(previous_status)
        target_layer = self._layer_for_status(status_after)
        status_changed = previous_status != status_after or previous_sub_status != sub_status_after

        order["current_status"] = status_after
        order["sub_status"] = sub_status_after
        order["current_layer"] = target_layer
        order["next_owner_agent"] = rule.get("next_owner_agent")
        order["blocked"] = rule.get("blocked", False)
        order["last_orchestration"] = {
            "event_type": payload["event_type"],
            "decision_summary": rule["decision_summary"],
            "status_before": previous_status,
            "status_after": status_after,
            "sub_status_before": previous_sub_status,
            "sub_status_after": sub_status_after,
            "current_layer": current_layer,
            "target_layer": target_layer,
            "blocked": rule.get("blocked", False),
            "next_owner_agent": rule.get("next_owner_agent"),
            "next_agents": subscribers,
        }
        self.store.save_order(order)

        result = {
            "applied": True,
            "status_changed": status_changed,
            "status_before": previous_status,
            "status_after": status_after,
            "sub_status_before": previous_sub_status,
            "sub_status_after": sub_status_after,
            "current_layer": current_layer,
            "target_layer": target_layer,
            "blocked": rule.get("blocked", False),
            "next_owner_agent": rule.get("next_owner_agent"),
            "next_agents": subscribers,
            "decision_summary": rule["decision_summary"],
        }
        self._log_run(order_id, payload["event_type"], payload, result)
        return result

    def _layer_for_status(self, status: str | None) -> str | None:
        if status is None:
            return None
        return self.status_layers.get(status)

    def _log_run(self, order_id: str, event_type: str, payload: dict, result: dict) -> None:
        self.agent_run_service.log_run(
            agent_name="Order Orchestrator",
            trigger_event_type=event_type,
            order_id=order_id,
            input_context=payload,
            output_result=result,
        )
