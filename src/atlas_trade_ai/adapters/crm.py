from __future__ import annotations

from atlas_trade_ai.adapters.base import AdapterHealth
from atlas_trade_ai.core.config_loader import JsonConfigLoader


class CRMAdapter:
    def __init__(self, loader: JsonConfigLoader | None = None) -> None:
        self.loader = loader or JsonConfigLoader()
        self.data = self.loader.load("mock_integrations.json")["crm"]

    def health(self) -> AdapterHealth:
        return AdapterHealth(
            name="纷享销客 CRM",
            connected=True,
            mode="mock-api",
            description=f"客户经营前台适配器，当前使用 Mock 数据，客户 {len(self.data['customers'])} 条。",
        )

    def list_customers(self) -> list[dict]:
        return self.data["customers"]

    def list_quotations(self) -> list[dict]:
        return self.data["quotations"]

    def list_followups(self) -> list[dict]:
        return self.data["followups"]
