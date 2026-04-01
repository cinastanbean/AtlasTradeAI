from __future__ import annotations

from atlas_trade_ai.core.bootstrap import build_seed_store
from atlas_trade_ai.core.config_loader import JsonConfigLoader
from atlas_trade_ai.services.agent_service import FollowUpAgentService
from atlas_trade_ai.services.context_builder_service import ContextBuilderService
from atlas_trade_ai.services.customer_service import CustomerService
from atlas_trade_ai.services.event_service import EventService
from atlas_trade_ai.services.exception_service import ExceptionService
from atlas_trade_ai.services.integration_service import IntegrationService
from atlas_trade_ai.services.notification_service import NotificationService
from atlas_trade_ai.services.order_service import OrderService
from atlas_trade_ai.services.overview_service import OverviewService
from atlas_trade_ai.services.rule_registry_service import RuleRegistryService
from atlas_trade_ai.services.task_service import TaskService
from atlas_trade_ai.services.workbench_service import WorkbenchService
from atlas_trade_ai.services.workflow_service import WorkflowService


class AppContainer:
    def __init__(self) -> None:
        self.store = build_seed_store()
        self.config_loader = JsonConfigLoader()
        self.rule_registry_service = RuleRegistryService(self.config_loader)
        self.customer_service = CustomerService(self.store)
        self.order_service = OrderService(self.store)
        self.task_service = TaskService(self.store)
        self.exception_service = ExceptionService(self.store)
        self.notification_service = NotificationService(self.store)
        self.follow_up_agent_service = FollowUpAgentService()
        self.context_builder_service = ContextBuilderService(self.store, self.order_service)
        self.workflow_service = WorkflowService(
            rule_registry=self.rule_registry_service,
            context_builder=self.context_builder_service,
            task_service=self.task_service,
            exception_service=self.exception_service,
            notification_service=self.notification_service,
            follow_up_agent_service=self.follow_up_agent_service,
        )
        self.event_service = EventService(
            store=self.store,
            workflow_service=self.workflow_service,
        )
        self.overview_service = OverviewService()
        self.workbench_service = WorkbenchService(self.store)
        self.integration_service = IntegrationService()


container = AppContainer()
