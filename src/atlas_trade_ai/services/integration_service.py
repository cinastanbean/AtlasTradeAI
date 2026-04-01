from __future__ import annotations

from dataclasses import asdict

from atlas_trade_ai.adapters.crm import CRMAdapter
from atlas_trade_ai.adapters.dingtalk import DingTalkAdapter
from atlas_trade_ai.adapters.erp import ERPAdapter


class IntegrationService:
    def __init__(self) -> None:
        self.adapters = [CRMAdapter(), ERPAdapter(), DingTalkAdapter()]

    def list_adapter_health(self) -> list[dict]:
        return [asdict(adapter.health()) for adapter in self.adapters]
