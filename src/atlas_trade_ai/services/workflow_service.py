from __future__ import annotations

from atlas_trade_ai.services.agent_service import FollowUpAgentService
from atlas_trade_ai.services.context_builder_service import ContextBuilderService
from atlas_trade_ai.services.exception_service import ExceptionService
from atlas_trade_ai.services.notification_service import NotificationService
from atlas_trade_ai.services.rule_registry_service import RuleRegistryService
from atlas_trade_ai.services.task_service import TaskService


class WorkflowService:
    def __init__(
        self,
        rule_registry: RuleRegistryService,
        context_builder: ContextBuilderService,
        task_service: TaskService,
        exception_service: ExceptionService,
        notification_service: NotificationService,
        follow_up_agent_service: FollowUpAgentService,
    ) -> None:
        self.rule_registry = rule_registry
        self.context_builder = context_builder
        self.task_service = task_service
        self.exception_service = exception_service
        self.notification_service = notification_service
        self.follow_up_agent_service = follow_up_agent_service

    def process_event(self, payload: dict) -> dict:
        rule = self.rule_registry.get_rule_for_event(payload["event_type"])
        if not rule or not payload.get("order_id"):
            return {
                "matched_rule": None,
                "generated_task_ids": [],
                "generated_exception_ids": [],
                "notification_ids": [],
            }

        context_payload = self.context_builder.build_follow_up_context(payload)
        agent_result = self.follow_up_agent_service.run(context_payload)

        generated_task_ids: list[str] = []
        generated_exception_ids: list[str] = []
        notification_ids: list[str] = []

        if rule.get("task_enabled"):
            assignee_id = context_payload["customer_context"].get("owner_id")
            for task in agent_result["task_drafts"]:
                created = self.task_service.create_task(
                    {
                        "task_type": "followup",
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
            assignee_id = context_payload["customer_context"].get("owner_id")
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
                    "template_code": rule["rule_code"],
                    "receiver_ids": [context_payload["customer_context"].get("owner_id") or "unassigned"],
                    "payload": {
                        "order_no": context_payload["order_context"]["order_no"],
                        "message": agent_result["notification_draft"],
                    },
                }
            )
            notification_ids.append(notification["notification_id"])

        return {
            "matched_rule": rule["rule_code"],
            "generated_task_ids": generated_task_ids,
            "generated_exception_ids": generated_exception_ids,
            "notification_ids": notification_ids,
        }
