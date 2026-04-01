from __future__ import annotations

from atlas_trade_ai.adapters.base import AdapterHealth


class CRMAdapter:
    def health(self) -> AdapterHealth:
        return AdapterHealth(
            name="纷享销客 CRM",
            connected=False,
            mode="placeholder",
            description="客户经营前台适配器，当前为结构占位。",
        )
