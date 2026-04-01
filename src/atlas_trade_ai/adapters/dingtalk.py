from __future__ import annotations

from atlas_trade_ai.adapters.base import AdapterHealth


class DingTalkAdapter:
    def health(self) -> AdapterHealth:
        return AdapterHealth(
            name="钉钉",
            connected=False,
            mode="placeholder",
            description="消息通知与待办触达适配器，当前为结构占位。",
        )
