from __future__ import annotations

from dataclasses import asdict

from atlas_trade_ai.core.config_loader import JsonConfigLoader
from atlas_trade_ai.adapters.crm import CRMAdapter
from atlas_trade_ai.adapters.dingtalk import DingTalkAdapter
from atlas_trade_ai.adapters.erp import ERPAdapter


class IntegrationService:
    def __init__(self) -> None:
        loader = JsonConfigLoader()
        self.crm = CRMAdapter(loader)
        self.erp = ERPAdapter(loader)
        self.dingtalk = DingTalkAdapter(loader)
        self.adapters = [self.crm, self.erp, self.dingtalk]

    def list_adapter_health(self) -> list[dict]:
        return [asdict(adapter.health()) for adapter in self.adapters]

    def get_crm_snapshot(self) -> dict:
        return {
            "customers": self.crm.list_customers(),
            "quotations": self.crm.list_quotations(),
            "followups": self.crm.list_followups(),
        }

    def get_erp_snapshot(self) -> dict:
        return {
            "orders": self.erp.list_orders(),
            "production": self.erp.list_production(),
            "payments": self.erp.list_payments(),
            "inventory": self.erp.list_inventory(),
        }

    def get_dingtalk_snapshot(self) -> dict:
        return {
            "todos": self.dingtalk.list_todos(),
            "messages": self.dingtalk.list_messages(),
            "approvals": self.dingtalk.list_approvals(),
        }
