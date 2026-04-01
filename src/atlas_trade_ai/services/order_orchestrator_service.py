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
        self.state_machine = config.get("state_machine", {})
        self.escalation_defaults = config.get("escalation_defaults", {})
        self.rules = {item["event_type"]: item for item in config["rules"]}
        org = loader.load("organization_directory.json")
        self.users = {item["user_id"]: item for item in org.get("users", [])}
        self.agent_owners = org.get("agent_owners", {})
        self.critical_watchers = org.get("critical_watchers", [])

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
                "sla_hours": None,
                "transition_allowed": True,
                "escalation": self._build_no_escalation(),
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
        transition_allowed = self._is_transition_allowed(previous_status, status_after, rule)
        escalation = self._evaluate_escalation(order, payload, rule, subscribers)
        status_changed = (
            transition_allowed
            and (previous_status != status_after or previous_sub_status != sub_status_after)
        )

        if transition_allowed:
            order["current_status"] = status_after
            order["sub_status"] = sub_status_after
            order["current_layer"] = target_layer
            order["next_owner_agent"] = rule.get("next_owner_agent")
            order["blocked"] = rule.get("blocked", False)
        else:
            status_after = previous_status
            sub_status_after = previous_sub_status
            target_layer = current_layer
            escalation = self._merge_with_transition_block(escalation, previous_status, payload["event_type"])

        order["last_orchestration"] = {
            "event_type": payload["event_type"],
            "decision_summary": self._compose_summary(rule["decision_summary"], transition_allowed, escalation),
            "status_before": previous_status,
            "status_after": status_after,
            "sub_status_before": previous_sub_status,
            "sub_status_after": sub_status_after,
            "current_layer": current_layer,
            "target_layer": target_layer,
            "blocked": rule.get("blocked", False),
            "sla_hours": rule.get("sla_hours"),
            "transition_allowed": transition_allowed,
            "escalation": escalation,
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
            "sla_hours": rule.get("sla_hours"),
            "transition_allowed": transition_allowed,
            "escalation": escalation,
            "next_owner_agent": rule.get("next_owner_agent"),
            "next_agents": subscribers,
            "decision_summary": self._compose_summary(rule["decision_summary"], transition_allowed, escalation),
        }
        self._log_run(order_id, payload["event_type"], payload, result)
        return result

    def _is_transition_allowed(self, previous_status: str | None, target_status: str, rule: dict) -> bool:
        allowed_from = rule.get("allowed_from")
        if allowed_from and previous_status not in allowed_from:
            return False
        if previous_status is None:
            return True
        allowed_targets = self.state_machine.get(previous_status, [])
        return target_status in allowed_targets if allowed_targets else True

    def _evaluate_escalation(
        self,
        order: dict,
        payload: dict,
        rule: dict,
        subscribers: list[str],
    ) -> dict:
        order_id = order["order_id"]
        same_event_count = len(
            [
                item
                for item in self.store.list_events()
                if item.get("order_id") == order_id and item.get("event_type") == payload["event_type"]
            ]
        )
        recent_event_types = {
            item.get("event_type")
            for item in self.store.list_events()
            if item.get("order_id") == order_id
        }
        open_exception_count = len(
            [
                item
                for item in self.store.list_exceptions()
                if item.get("related_order_id") == order_id and item.get("exception_status") != "已解决"
            ]
        )
        priority = payload.get("priority")
        customer_level = self.store.get_customer(order["customer_id"]).get("customer_level")
        repeat_threshold = rule.get(
            "repeat_event_threshold",
            self.escalation_defaults.get("repeat_event_threshold", 2),
        )
        exception_threshold = rule.get(
            "open_exception_threshold",
            self.escalation_defaults.get("open_exception_threshold", 2),
        )

        level = "none"
        reasons: list[str] = []
        targets: list[str] = []
        composite_signals: list[str] = []
        if rule.get("blocked") and rule.get("escalation_strategy") == "immediate":
            level = "high"
            reasons.append("当前事件会阻塞订单推进，需立即升级处理")
            targets.extend([rule.get("next_owner_agent"), "follow_up_agent"])
        if same_event_count >= repeat_threshold:
            level = "critical" if level == "high" else "high"
            reasons.append(f"同类事件已累计触发 {same_event_count} 次")
            targets.extend(["order_orchestrator", rule.get("next_owner_agent")])
        if open_exception_count >= exception_threshold:
            level = "critical" if level in {"high", "medium"} else "high"
            reasons.append(f"当前订单已有 {open_exception_count} 条未解决异常")
            targets.extend(["follow_up_agent", rule.get("next_owner_agent")])
        if priority == "P1":
            level = "critical" if level == "high" else (level if level != "none" else "high")
            reasons.append("事件优先级为 P1")
        if customer_level in {"战略客户", "重点客户"} and rule.get("blocked"):
            level = "critical" if level in {"high", "medium"} else "high"
            reasons.append(f"客户等级为 {customer_level}，需提高处理关注度")
        if {"production.milestone_delayed", "document.missing"}.issubset(recent_event_types):
            level = "critical"
            reasons.append("生产异常与单证异常同时存在，形成跨层阻塞")
            composite_signals.append("cross_layer_blocking")
            targets.extend(["supply_chain_agent", "customs_agent", "follow_up_agent"])
        if {"logistics.delayed", "payment.overdue"}.issubset(recent_event_types):
            level = "critical"
            reasons.append("物流延误与回款逾期同时存在，形成交付与资金复合风险")
            composite_signals.append("delivery_finance_compound_risk")
            targets.extend(["logistics_agent", "finance_agent", "follow_up_agent"])
        if len(composite_signals) >= 1 and "order_orchestrator" not in targets:
            targets.append("order_orchestrator")

        unique_targets = [item for item in dict.fromkeys(targets) if item]
        if level == "none":
            return self._build_no_escalation()
        resolved_targets = self._resolve_targets(unique_targets, order)
        return {
            "level": level,
            "required": True,
            "reasons": reasons,
            "targets": unique_targets,
            "resolved_targets": resolved_targets,
            "composite_signals": composite_signals,
        }

    def _build_no_escalation(self) -> dict:
        return {
            "level": "none",
            "required": False,
            "reasons": [],
            "targets": [],
            "resolved_targets": [],
            "composite_signals": [],
        }

    def _merge_with_transition_block(self, escalation: dict, previous_status: str | None, event_type: str) -> dict:
        reasons = list(escalation.get("reasons", []))
        reasons.append(f"事件 {event_type} 不允许从当前状态 {previous_status} 直接推进")
        targets = list(dict.fromkeys(escalation.get("targets", []) + ["order_orchestrator"]))
        level = escalation.get("level", "none")
        if level == "none":
            level = "high"
        elif level == "high":
            level = "critical"
        return {
            "level": level,
            "required": True,
            "reasons": reasons,
            "targets": targets,
            "resolved_targets": self._resolve_targets(targets, {"owner_id": None, "customer_id": None}),
            "composite_signals": escalation.get("composite_signals", []),
        }

    def _compose_summary(self, base_summary: str, transition_allowed: bool, escalation: dict) -> str:
        parts = [base_summary]
        if not transition_allowed:
            parts.append("本次状态推进未通过状态机校验，已保持原阶段。")
        if escalation.get("required"):
            parts.append(f"已触发 {escalation['level']} 级升级。")
        return "".join(parts)

    def _resolve_targets(self, targets: list[str], order: dict) -> list[dict]:
        owner_id = order.get("owner_id")
        if owner_id is None and order.get("customer_id"):
            owner_id = self.store.get_customer(order["customer_id"]).get("owner_id")
        resolved: list[dict] = []
        for target in targets:
            user_ids = list(self.agent_owners.get(target, []))
            if target in {"follow_up_agent", "sales_agent", "crm_agent"} and owner_id:
                user_ids = [owner_id] + user_ids
            if target == "order_orchestrator":
                user_ids = user_ids + self.critical_watchers
            for user_id in dict.fromkeys([item for item in user_ids if item]):
                user = self.users.get(user_id, {"user_id": user_id, "name": user_id, "role": "未知角色"})
                resolved.append(
                    {
                        "target": target,
                        "user_id": user_id,
                        "user_name": user["name"],
                        "role": user["role"],
                    }
                )
        return resolved

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
