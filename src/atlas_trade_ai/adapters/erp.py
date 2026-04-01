from __future__ import annotations

from atlas_trade_ai.adapters.base import AdapterHealth
from atlas_trade_ai.core.config_loader import JsonConfigLoader


class ERPAdapter:
    def __init__(self, loader: JsonConfigLoader | None = None) -> None:
        self.loader = loader or JsonConfigLoader()
        self.data = self.loader.load("mock_integrations.json")["erp"]

    def health(self) -> AdapterHealth:
        return AdapterHealth(
            name="金蝶云星空 ERP",
            connected=True,
            mode="mock-api",
            description=f"订单、库存、采购、财务主干系统适配器，当前使用 Mock 数据，订单 {len(self.data['orders'])} 条。",
        )

    def list_orders(self) -> list[dict]:
        return self.data["orders"]

    def list_production(self) -> list[dict]:
        return self.data["production"]

    def list_payments(self) -> list[dict]:
        return self.data["payments"]

    def list_inventory(self) -> list[dict]:
        return self.data["inventory"]
