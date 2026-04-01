from __future__ import annotations

from atlas_trade_ai.services.agent_registry_service import AgentRegistryService
from atlas_trade_ai.services.context_builder_service import ContextBuilderService
from atlas_trade_ai.services.exception_service import ExceptionService
from atlas_trade_ai.services.notification_service import NotificationService
from atlas_trade_ai.services.order_orchestrator_service import OrderOrchestratorService
from atlas_trade_ai.services.rule_registry_service import RuleRegistryService
from atlas_trade_ai.services.task_service import TaskService


class WorkflowService:
    def __init__(
        self,
        rule_registry: RuleRegistryService,
        agent_registry: AgentRegistryService,
        order_orchestrator: OrderOrchestratorService,
        context_builder: ContextBuilderService,
        task_service: TaskService,
        exception_service: ExceptionService,
        notification_service: NotificationService,
    ) -> None:
        self.rule_registry = rule_registry
        self.agent_registry = agent_registry
        self.order_orchestrator = order_orchestrator
        self.context_builder = context_builder
        self.task_service = task_service
        self.exception_service = exception_service
        self.notification_service = notification_service

    def process_event(self, payload: dict) -> dict:
        rule = self.rule_registry.get_rule_for_event(payload["event_type"])
        if not rule or not payload.get("order_id"):
            return {
                "matched_rule": None,
                "orchestration": None,
                "generated_task_ids": [],
                "generated_exception_ids": [],
                "notification_ids": [],
            }

        orchestration = self.order_orchestrator.orchestrate(
            payload,
            rule.get("subscribers", []),
        )
        context_payload = self.context_builder.build_follow_up_context(payload)

        generated_task_ids: list[str] = []
        generated_exception_ids: list[str] = []
        notification_ids: list[str] = []
        orchestration_escalation = (orchestration or {}).get("escalation") or {}
        if orchestration_escalation.get("required"):
            for target in orchestration_escalation.get("resolved_targets", []):
                escalation_task = self.task_service.create_task(
                    {
                        "task_type": "order_orchestrator_escalation",
                        "task_title": f"处理中枢升级：{context_payload['order_context']['order_no']}",
                        "task_description": orchestration["decision_summary"],
                        "related_order_id": context_payload["order_context"]["order_id"],
                        "assignee_id": target.get("user_id"),
                        "priority": "high" if orchestration_escalation.get("level") in {"high", "critical"} else "medium",
                        "due_time": f"{orchestration.get('sla_hours') or 4}小时内",
                    }
                )
                generated_task_ids.append(escalation_task["task_id"])
            escalation_receivers = [
                item["user_id"]
                for item in orchestration_escalation.get("resolved_targets", [])
                if item.get("user_id")
            ]
            if escalation_receivers:
                escalation_notification = self.notification_service.send_dingtalk(
                    {
                        "template_code": f"ORCH_ESCALATION_{payload['event_type']}",
                        "receiver_ids": escalation_receivers,
                        "payload": {
                            "order_no": context_payload["order_context"]["order_no"],
                            "message": orchestration["decision_summary"],
                            "escalation_level": orchestration_escalation.get("level"),
                            "targets": orchestration_escalation.get("targets", []),
                        },
                    }
                )
                notification_ids.append(escalation_notification["notification_id"])
        for agent_key in rule.get("subscribers", []):
            agent_service = self.agent_registry.get_agent_service(agent_key)
            if agent_service is None:
                continue
            agent_result = agent_service.run(context_payload)
            assignee_id = context_payload["customer_context"].get("owner_id")

            if rule.get("task_enabled"):
                for task in agent_result["task_drafts"]:
                    created = self.task_service.create_task(
                        {
                            "task_type": agent_key,
                            "task_title": task["title"],
                            "task_description": agent_result["summary"],
                            "related_order_id": context_payload["order_context"]["order_id"],
                            "assignee_id": assignee_id,
                            "priority": task["priority"],
                            "due_time": task["due_hint"],
                        }
                    )
                    generated_task_ids.append(created["task_id"])

            if rule.get("exception_enabled"):
                for exception in agent_result["exception_marks"]:
                    created = self.exception_service.create_exception(
                        {
                            "exception_type": exception["exception_type"],
                            "exception_level": exception["exception_level"],
                            "related_order_id": context_payload["order_context"]["order_id"],
                            "source_event_id": payload["event_id"],
                            "owner_id": assignee_id,
                            "suggestion": exception["reason"],
                        }
                    )
                    generated_exception_ids.append(created["exception_id"])

            if rule.get("notification_enabled"):
                notification = self.notification_service.send_dingtalk(
                    {
                        "template_code": f"{rule['rule_code']}_{agent_key}",
                        "receiver_ids": [assignee_id or "unassigned"],
                        "payload": {
                            "order_no": context_payload["order_context"]["order_no"],
                            "message": agent_result["notification_draft"],
                            "agent_name": agent_key,
                        },
                    }
                )
                notification_ids.append(notification["notification_id"])

        return {
            "matched_rule": rule["rule_code"],
            "orchestration": orchestration,
            "generated_task_ids": generated_task_ids,
            "generated_exception_ids": generated_exception_ids,
            "notification_ids": notification_ids,
        }
