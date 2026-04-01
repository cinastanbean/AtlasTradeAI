from __future__ import annotations

from atlas_trade_ai.adapters.base import AdapterHealth


class ERPAdapter:
    def health(self) -> AdapterHealth:
        return AdapterHealth(
            name="金蝶云星空 ERP",
            connected=False,
            mode="placeholder",
            description="订单、库存、采购、财务主干系统适配器，当前为结构占位。",
        )
